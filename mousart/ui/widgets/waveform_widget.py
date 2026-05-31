"""UART serial waveform rendering widget using QPainter.

Draws the actual serial signal waveform:
  Idle(High) → Start(Low) → D0..D7 → Stop(High) → Idle(High)
Each byte becomes 10 bit-periods (8N1 format).
"""
from mousart.qt_compat import *


class WaveformWidget(QWidget):
    """UART serial protocol waveform display."""

    DEFAULT_BUFFER_SIZE = 64  # max bytes in buffer

    def __init__(self, parent=None, theme_manager=None, buffer_size=None,
                 data_bits=8, parity='N', stop_bits=1):
        super().__init__(parent)
        self._theme_manager = theme_manager
        self._buffer_size = buffer_size or self.DEFAULT_BUFFER_SIZE

        # UART config
        self._data_bits = data_bits      # 5, 6, 7, 8
        self._parity = parity            # 'N', 'E', 'O'
        self._stop_bits = stop_bits      # 1, 1.5, 2

        # Bits per frame: start(1) + data + parity(0 or 1) + stop
        self._parity_bits = 0 if parity == 'N' else 1
        self._stop_bit_count = stop_bits  # 1, 1.5, or 2
        self._bits_per_frame = 1 + data_bits + self._parity_bits + self._stop_bit_count

        # Data storage
        self._data = bytearray()
        self._direction = "RX"
        self._is_realtime = False

        # View state
        self._x_offset = 0.0     # bit index offset
        self._x_scale = 8.0      # pixels per bit (zoom level)

        # Mouse
        self._mouse_pos = None
        self._dragging = False
        self._drag_start = None
        self._drag_offset_start = 0.0

        # Layout
        self._margin_left = 36
        self._margin_right = 12
        self._margin_top = 20
        self._margin_bottom = 24

        self.setMinimumHeight(100)
        self.setMinimumWidth(200)
        self.setMouseTracking(True)

    def set_theme_manager(self, tm):
        self._theme_manager = tm
        self.update()

    def set_direction(self, direction: str):
        self._direction = direction
        self.update()

    def set_realtime(self, enabled: bool):
        self._is_realtime = enabled

    def set_uart_config(self, data_bits=8, parity='N', stop_bits=1):
        self._data_bits = data_bits
        self._parity = parity
        self._stop_bits = stop_bits
        self._parity_bits = 0 if parity == 'N' else 1
        self._stop_bit_count = stop_bits
        self._bits_per_frame = 1 + data_bits + self._parity_bits + self._stop_bit_count
        self.update()

    def set_data(self, data: bytes, direction: str = "RX"):
        self._data = bytearray(data)
        self._direction = direction
        self._is_realtime = False
        self._x_offset = 0
        self._auto_fit()
        self.update()

    def append_data(self, data: bytes):
        try:
            if not data:
                return
            self._data.extend(data)
            if len(self._data) > self._buffer_size:
                self._data = self._data[len(self._data) - self._buffer_size:]
            # Auto-scroll to end
            total_bits = len(self._data) * self._bits_per_frame
            plot_w = self.width() - self._margin_left - self._margin_right
            visible_bits = plot_w / self._x_scale
            self._x_offset = max(0, total_bits - visible_bits)
            self.update()
        except Exception:
            pass

    def clear(self):
        self._data.clear()
        self._x_offset = 0
        self.update()

    def _auto_fit(self):
        if not self._data:
            return
        total_bits = len(self._data) * self._bits_per_frame
        plot_w = self.width() - self._margin_left - self._margin_right
        if plot_w < 1:
            plot_w = 1
        self._x_scale = max(4.0, plot_w / max(1, total_bits))
        self._x_offset = 0

    # --- Byte to bit levels ---

    def _byte_to_levels(self, byte_val):
        """Convert a byte to a list of signal levels (0 or 1) for one frame.

        Returns list of (level, bit_label) tuples.
        Level 1 = HIGH, Level 0 = LOW.
        """
        levels = []

        # Start bit: always LOW
        levels.append((0, 'S'))

        # Data bits (LSB first)
        for i in range(self._data_bits):
            bit = (byte_val >> i) & 1
            levels.append((bit, f'D{i}'))

        # Parity bit
        if self._parity_bits:
            if self._parity == 'E':  # even parity
                p = 0
                for i in range(self._data_bits):
                    p ^= (byte_val >> i) & 1
                levels.append((p, 'P'))
            elif self._parity == 'O':  # odd parity
                p = 1
                for i in range(self._data_bits):
                    p ^= (byte_val >> i) & 1
                levels.append((p, 'P'))

        # Stop bits: always HIGH
        if self._stop_bit_count == 1:
            levels.append((1, 'St'))
        elif self._stop_bit_count == 2:
            levels.append((1, 'St'))
            levels.append((1, 'St'))
        elif self._stop_bit_count == 1.5:
            # 1.5 stop bits: draw as 1.5 bit periods of HIGH
            levels.append((1, 'St'))
            levels.append((1, 'St'))  # will render with special handling

        return levels

    # --- Painting ---

    def paintEvent(self, event):
        try:
            self._paint_impl(event)
        except Exception:
            pass

    def _paint_impl(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()

        # Colors
        if self._theme_manager:
            bg = self._theme_manager.get_color("receiveBg")
            grid_color = self._theme_manager.get_color("border")
            text_color = self._theme_manager.get_color("textSecondary")
        else:
            bg = QColor("#0d1117")
            grid_color = QColor("#2a2a4a")
            text_color = QColor("#8899aa")

        wave_color = QColor("#569cd6") if self._direction == "TX" else QColor("#4ec9b0")
        idle_color = QColor("#8899aa")

        painter.fillRect(0, 0, w, h, bg)

        pl = self._margin_left
        pt = self._margin_top
        pr = w - self._margin_right
        pb = h - self._margin_bottom
        plot_w = pr - pl
        plot_h = pb - pt

        if plot_w < 1 or plot_h < 1 or not self._data:
            self._draw_labels(painter, pl, pt, pr, pb, text_color)
            painter.end()
            return

        painter.setClipRect(pl, pt, int(plot_w), int(plot_h))

        # Signal levels
        high_y = pt + plot_h * 0.15
        low_y = pt + plot_h * 0.85
        mid_y = pt + plot_h * 0.5

        # --- Draw horizontal reference lines ---
        ref_pen = QPen(grid_color)
        ref_pen.setWidth(1)
        ref_pen.setStyle(Qt.PenStyle.DashLine)
        painter.setPen(ref_pen)
        painter.drawLine(int(pl), int(high_y), int(pr), int(high_y))
        painter.drawLine(int(pl), int(low_y), int(pr), int(low_y))

        # --- Draw UART waveform ---
        wave_pen = QPen(wave_color)
        wave_pen.setWidth(2)
        wave_pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        wave_pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(wave_pen)

        bit_idx = 0  # global bit index
        for byte_val in self._data:
            levels = self._byte_to_levels(byte_val)
            for i, (level, label) in enumerate(levels):
                x_start = pl + (bit_idx - self._x_offset) * self._x_scale
                x_end = pl + (bit_idx + 1 - self._x_offset) * self._x_scale

                # Skip if outside visible area
                if x_end < pl - 2 or x_start > pr + 2:
                    bit_idx += 1
                    continue

                y = high_y if level else low_y

                # Draw vertical transition edge (except at frame start)
                if i > 0:
                    prev_level = levels[i - 1][0]
                    if prev_level != level:
                        painter.drawLine(int(x_start), int(high_y if prev_level else low_y),
                                         int(x_start), int(y))

                # Draw horizontal line for this bit
                painter.drawLine(int(x_start), int(y), int(x_end), int(y))

                # Draw bit label
                if self._x_scale >= 10 and x_start >= pl - 2 and x_end <= pr + 2:
                    label_pen = QPen(text_color)
                    label_pen.setWidth(1)
                    painter.setPen(label_pen)
                    font = painter.font()
                    font.setPointSize(7)
                    painter.setFont(font)
                    lx = (x_start + x_end) / 2 - 4
                    ly = low_y + 14 if level else high_y - 6
                    painter.drawText(int(lx), int(ly), label)
                    wave_pen.setWidth(2)
                    painter.setPen(wave_pen)

                bit_idx += 1

        # --- Frame separators (dashed vertical lines between bytes) ---
        sep_pen = QPen(grid_color)
        sep_pen.setWidth(1)
        sep_pen.setStyle(Qt.PenStyle.DotLine)
        painter.setPen(sep_pen)
        for byte_idx in range(1, len(self._data)):
            x = pl + (byte_idx * self._bits_per_frame - self._x_offset) * self._x_scale
            if pl <= x <= pr:
                painter.drawLine(int(x), int(pt), int(x), int(pb))

        # --- Crosshair ---
        painter.setClipping(False)
        if self._mouse_pos and self._rect_contains(self._mouse_pos, pl, pt, pr, pb):
            mx = self._mouse_pos.x()
            cross_pen = QPen(text_color)
            cross_pen.setWidth(1)
            cross_pen.setStyle(Qt.PenStyle.DotLine)
            painter.setPen(cross_pen)
            painter.drawLine(int(mx), int(pt), int(mx), int(pb))

            # Show which byte/bit the cursor is over
            bit_at_cursor = (mx - pl) / self._x_scale + self._x_offset
            byte_idx = int(bit_at_cursor / self._bits_per_frame)
            bit_in_frame = bit_at_cursor - byte_idx * self._bits_per_frame
            if 0 <= byte_idx < len(self._data):
                bv = self._data[byte_idx]
                levels = self._byte_to_levels(bv)
                bit_pos = int(bit_in_frame)
                if 0 <= bit_pos < len(levels):
                    lbl = levels[bit_pos][1]
                    info = f"字节[{byte_idx}] = 0x{bv:02X} ({bv:08b})  位: {lbl}"
                else:
                    info = f"字节[{byte_idx}] = 0x{bv:02X} ({bv:08b})"
                painter.setPen(QPen(QColor("#ffffff")))
                font = painter.font()
                font.setPointSize(9)
                painter.setFont(font)
                painter.drawText(int(mx) + 8, int(pt) + 14, info)

        self._draw_labels(painter, pl, pt, pr, pb, text_color)
        painter.end()

    def _draw_labels(self, painter, pl, pt, pr, pb, text_color):
        painter.setClipping(False)
        painter.setPen(QPen(text_color))
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)

        h = pb - pt
        high_y = pt + h * 0.15
        low_y = pt + h * 0.85

        # Y-axis labels
        painter.drawText(2, int(high_y) + 4, "1")
        painter.drawText(2, int(low_y) + 4, "0")

        # X-axis info
        if self._data:
            info = f"字节: {len(self._data)}"
            if self._is_realtime:
                info += f" / {self._buffer_size}  实时"
            painter.drawText(pl, self.height() - 4, info)

    @staticmethod
    def _rect_contains(pos, pl, pt, pr, pb):
        return pl <= pos.x() <= pr and pt <= pos.y() <= pb

    # --- Mouse ---

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._dragging = True
            self._drag_start = event.position()
            self._drag_offset_start = self._x_offset
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._dragging = False
        self._drag_start = None
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        pos = event.position()
        self._mouse_pos = pos
        if self._dragging and self._drag_start is not None:
            dx = pos.x() - self._drag_start.x()
            self._x_offset = max(0, self._drag_offset_start - dx / self._x_scale)
        self.update()
        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._mouse_pos = None
        self.update()
        super().leaveEvent(event)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        factor = 0.85 if delta > 0 else 1.15
        old_scale = self._x_scale
        self._x_scale = max(2.0, min(40.0, self._x_scale * factor))
        if self._mouse_pos:
            mx = self._mouse_pos.x()
            pl = self._margin_left
            bit_at = (mx - pl) / old_scale + self._x_offset
            self._x_offset = max(0, bit_at - (mx - pl) / self._x_scale)
        self.update()
        super().wheelEvent(event)

    def resizeEvent(self, event):
        if not self._is_realtime and self._data:
            self._auto_fit()
        super().resizeEvent(event)
