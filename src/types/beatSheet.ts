export interface SceneProps {
  renderMode?: "full" | "ui_only_alpha";
}

export interface SfxConfig {
  sample: string;
  frame_offset: number;
  volume_db: number;
  duration_in_frames?: number;
}

export interface SpringConfig {
  damping: number;
  stiffness: number;
  mass: number;
}

export interface LayoutConfig {
  x_offset: number;
  y_offset: number;
  scale: number;
  opacity: number;
}

export interface CaptionWord {
  text: string;
  start_frame: number;
  end_frame: number;
}

export interface ChartItem {
  label: string;
  value: number;
}

export interface SceneData {
  id: string;
  name: string;
  start_frame: number;
  duration_in_frames: number;
  title: string;
  subtitle?: string;
  badge?: string;
  accent_word?: string;
  author_name?: string;
  author_role?: string;
  layout: LayoutConfig;
  spring_config: SpringConfig;
  sfx?: SfxConfig;
  captions?: CaptionWord[];
  chart_data?: ChartItem[];
}

export interface GlobalStyles {
  font_family_headline: string;
  font_family_body: string;
  color_primary: string;
  color_background: string;
  color_accent: string;
  color_card_bg: string;
  color_text: string;
}

export interface BeatSheet {
  project_id: string;
  title: string;
  target_duration_sec: number;
  fps: number;
  width: number;
  height: number;
  render_mode?: "full" | "ui_only_alpha";
  global_styles: GlobalStyles;
  scenes: SceneData[];
}
