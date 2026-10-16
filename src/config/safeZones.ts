export interface Rect {
  left: number;
  top: number;
  right: number;
  bottom: number;
}

export const FRAME = { width: 1080, height: 1920 } as const;

export const SAFE_RECT: Rect = { left: 100, top: 220, right: 950, bottom: 1540 };

export const CAPTION_RECT: Rect = { left: 100, top: 1120, right: 950, bottom: 1380 };

export const shrinkForCamera = (rect: Rect, scale = 1, shiftX = 0): Rect => {
  const s = Math.max(1, scale);
  const cx = FRAME.width / 2;
  const cy = FRAME.height / 2;
  return {
    left: cx - (cx - rect.left) / s + Math.abs(shiftX),
    right: cx + (rect.right - cx) / s - Math.abs(shiftX),
    top: cy - (cy - rect.top) / s,
    bottom: cy + (rect.bottom - cy) / s,
  };
};
