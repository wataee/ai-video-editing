import { staticFile } from "remotion";

export interface SfxAsset {
  readonly id: string;
  readonly name: string;
  readonly path: string;
  readonly file: string;
  readonly category: "whooshes" | "textures" | "pops" | "sciFi" | "impacts" | "risers" | "ambience";
  readonly defaultVolume: number;
}

export interface FontAsset {
  readonly family: string;
  readonly weights: readonly string[];
  readonly regular: string;
  readonly italic?: string;
  readonly bold?: string;
}

export const SFX_WHOOSHES = {
  deepVoice01: {
    id: "deep_voice_whoosh_01",
    name: "Deep Voice Whoosh 01",
    path: "assets/01_SFX/01_whooshes/deep_voice/deep_voice_whoosh_01.wav",
    file: staticFile("assets/01_SFX/01_whooshes/deep_voice/deep_voice_whoosh_01.wav"),
    category: "whooshes",
    defaultVolume: 0.35,
  },
  deepVoice02: {
    id: "deep_voice_whoosh_02",
    name: "Deep Voice Whoosh 02",
    path: "assets/01_SFX/01_whooshes/deep_voice/deep_voice_whoosh_02.wav",
    file: staticFile("assets/01_SFX/01_whooshes/deep_voice/deep_voice_whoosh_02.wav"),
    category: "whooshes",
    defaultVolume: 0.35,
  },
  deepVoice03: {
    id: "deep_voice_whoosh_03",
    name: "Deep Voice Whoosh 03",
    path: "assets/01_SFX/01_whooshes/deep_voice/deep_voice_whoosh_03.wav",
    file: staticFile("assets/01_SFX/01_whooshes/deep_voice/deep_voice_whoosh_03.wav"),
    category: "whooshes",
    defaultVolume: 0.35,
  },
  cleanFast: {
    id: "whoosh_clean_fast",
    name: "Whoosh Clean Fast",
    path: "assets/01_SFX/01_whooshes/futuristic/whoosh_clean_fast.wav",
    file: staticFile("assets/01_SFX/01_whooshes/futuristic/whoosh_clean_fast.wav"),
    category: "whooshes",
    defaultVolume: 0.30,
  },
  hollow01: {
    id: "hollow_whoosh_01",
    name: "Hollow Whoosh 01",
    path: "assets/01_SFX/01_whooshes/hollow/hollow_whoosh_01.wav",
    file: staticFile("assets/01_SFX/01_whooshes/hollow/hollow_whoosh_01.wav"),
    category: "whooshes",
    defaultVolume: 0.30,
  },
  hollow02: {
    id: "hollow_whoosh_02",
    name: "Hollow Whoosh 02",
    path: "assets/01_SFX/01_whooshes/hollow/hollow_whoosh_02.wav",
    file: staticFile("assets/01_SFX/01_whooshes/hollow/hollow_whoosh_02.wav"),
    category: "whooshes",
    defaultVolume: 0.30,
  },
  subtleAir: {
    id: "whoosh_subtle_air",
    name: "Whoosh Subtle Air",
    path: "assets/01_SFX/01_whooshes/organic_wind/whoosh_subtle_air.wav",
    file: staticFile("assets/01_SFX/01_whooshes/organic_wind/whoosh_subtle_air.wav"),
    category: "whooshes",
    defaultVolume: 0.25,
  },
  syntheticTransition: {
    id: "synthetic_transition_whoosh",
    name: "Synthetic Transition Whoosh",
    path: "assets/01_SFX/01_whooshes/transitions/synthetic_transition_whoosh.wav",
    file: staticFile("assets/01_SFX/01_whooshes/transitions/synthetic_transition_whoosh.wav"),
    category: "whooshes",
    defaultVolume: 0.32,
  },
  transitionSpacey: {
    id: "transition_spacey_whoosh",
    name: "Transition Spacey Whoosh",
    path: "assets/01_SFX/01_whooshes/transitions/transition_spacey_whoosh.wav",
    file: staticFile("assets/01_SFX/01_whooshes/transitions/transition_spacey_whoosh.wav"),
    category: "whooshes",
    defaultVolume: 0.32,
  },
} as const;

export const SFX_TEXTURES = {
  cameraClickFast: {
    id: "camera_click_fast",
    name: "Camera Click Fast",
    path: "assets/01_SFX/02_textures/camera_shutter/camera_click_fast.wav",
    file: staticFile("assets/01_SFX/02_textures/camera_shutter/camera_click_fast.wav"),
    category: "textures",
    defaultVolume: 0.28,
  },
  click01: {
    id: "click_01",
    name: "Click 01",
    path: "assets/01_SFX/02_textures/clicks_ui/click_01.wav",
    file: staticFile("assets/01_SFX/02_textures/clicks_ui/click_01.wav"),
    category: "textures",
    defaultVolume: 0.22,
  },
  click02: {
    id: "click_02",
    name: "Click 02",
    path: "assets/01_SFX/02_textures/clicks_ui/click_02.wav",
    file: staticFile("assets/01_SFX/02_textures/clicks_ui/click_02.wav"),
    category: "textures",
    defaultVolume: 0.22,
  },
  mechanicalButton: {
    id: "mechanical_button",
    name: "Mechanical Button",
    path: "assets/01_SFX/02_textures/clicks_ui/mechanical_button.wav",
    file: staticFile("assets/01_SFX/02_textures/clicks_ui/mechanical_button.wav"),
    category: "textures",
    defaultVolume: 0.25,
  },
  mouseClickSoft: {
    id: "mouse_click_soft",
    name: "Mouse Click Soft",
    path: "assets/01_SFX/02_textures/clicks_ui/mouse_click_soft.wav",
    file: staticFile("assets/01_SFX/02_textures/clicks_ui/mouse_click_soft.wav"),
    category: "textures",
    defaultVolume: 0.20,
  },
  select01: {
    id: "select_01",
    name: "Select 01",
    path: "assets/01_SFX/02_textures/clicks_ui/select_01.wav",
    file: staticFile("assets/01_SFX/02_textures/clicks_ui/select_01.wav"),
    category: "textures",
    defaultVolume: 0.22,
  },
  switch01: {
    id: "switch_01",
    name: "Switch 01",
    path: "assets/01_SFX/02_textures/clicks_ui/switch_01.wav",
    file: staticFile("assets/01_SFX/02_textures/clicks_ui/switch_01.wav"),
    category: "textures",
    defaultVolume: 0.24,
  },
  complexGizmo: {
    id: "complex_mechanism_gizmo",
    name: "Complex Mechanism Gizmo",
    path: "assets/01_SFX/02_textures/gears_typewriter/complex_mechanism_gizmo.wav",
    file: staticFile("assets/01_SFX/02_textures/gears_typewriter/complex_mechanism_gizmo.wav"),
    category: "textures",
    defaultVolume: 0.25,
  },
  scratch01: {
    id: "scratch_01",
    name: "Scratch 01",
    path: "assets/01_SFX/02_textures/gears_typewriter/scratch_01.wav",
    file: staticFile("assets/01_SFX/02_textures/gears_typewriter/scratch_01.wav"),
    category: "textures",
    defaultVolume: 0.22,
  },
  scratch02: {
    id: "scratch_02",
    name: "Scratch 02",
    path: "assets/01_SFX/02_textures/gears_typewriter/scratch_02.wav",
    file: staticFile("assets/01_SFX/02_textures/gears_typewriter/scratch_02.wav"),
    category: "textures",
    defaultVolume: 0.22,
  },
  tinyGearwheelLoop: {
    id: "tiny_gearwheel_loop",
    name: "Tiny Gearwheel Loop",
    path: "assets/01_SFX/02_textures/gears_typewriter/tiny_gearwheel_loop.wav",
    file: staticFile("assets/01_SFX/02_textures/gears_typewriter/tiny_gearwheel_loop.wav"),
    category: "textures",
    defaultVolume: 0.18,
  },
} as const;

export const SFX_POPS = {
  glassPop: {
    id: "glass_pop",
    name: "Glass Pop",
    path: "assets/01_SFX/02_textures/pops/glass_pop.wav",
    file: staticFile("assets/01_SFX/02_textures/pops/glass_pop.wav"),
    category: "pops",
    defaultVolume: 0.28,
  },
  pop01: {
    id: "pop_01",
    name: "Pop 01",
    path: "assets/01_SFX/02_textures/pops/pop_01.wav",
    file: staticFile("assets/01_SFX/02_textures/pops/pop_01.wav"),
    category: "pops",
    defaultVolume: 0.25,
  },
  pop02: {
    id: "pop_02",
    name: "Pop 02",
    path: "assets/01_SFX/02_textures/pops/pop_02.wav",
    file: staticFile("assets/01_SFX/02_textures/pops/pop_02.wav"),
    category: "pops",
    defaultVolume: 0.25,
  },
  popBubbleHigh: {
    id: "pop_bubble_high",
    name: "Pop Bubble High",
    path: "assets/01_SFX/02_textures/pops/pop_bubble_high.wav",
    file: staticFile("assets/01_SFX/02_textures/pops/pop_bubble_high.wav"),
    category: "pops",
    defaultVolume: 0.24,
  },
  popCartoonClean: {
    id: "pop_cartoon_clean",
    name: "Pop Cartoon Clean",
    path: "assets/01_SFX/02_textures/pops/pop_cartoon_clean.wav",
    file: staticFile("assets/01_SFX/02_textures/pops/pop_cartoon_clean.wav"),
    category: "pops",
    defaultVolume: 0.26,
  },
} as const;

export const SFX_SCIFI = {
  activateEnergyHit: {
    id: "activate_energy_hit",
    name: "Activate Energy Hit",
    path: "assets/01_SFX/02_textures/sci_fi_hits/activate_energy_hit.wav",
    file: staticFile("assets/01_SFX/02_textures/sci_fi_hits/activate_energy_hit.wav"),
    category: "sciFi",
    defaultVolume: 0.32,
  },
  glitch01: {
    id: "glitch_01",
    name: "Glitch 01",
    path: "assets/01_SFX/02_textures/sci_fi_hits/glitch_01.wav",
    file: staticFile("assets/01_SFX/02_textures/sci_fi_hits/glitch_01.wav"),
    category: "sciFi",
    defaultVolume: 0.25,
  },
  glitch02: {
    id: "glitch_02",
    name: "Glitch 02",
    path: "assets/01_SFX/02_textures/sci_fi_hits/glitch_02.wav",
    file: staticFile("assets/01_SFX/02_textures/sci_fi_hits/glitch_02.wav"),
    category: "sciFi",
    defaultVolume: 0.25,
  },
  sciFiImpactReveal: {
    id: "sci_fi_impact_reveal",
    name: "Sci-Fi Impact Reveal",
    path: "assets/01_SFX/02_textures/sci_fi_hits/sci_fi_impact_reveal.wav",
    file: staticFile("assets/01_SFX/02_textures/sci_fi_hits/sci_fi_impact_reveal.wav"),
    category: "sciFi",
    defaultVolume: 0.35,
  },
} as const;

export const SFX_IMPACTS = {
  bassDrop01: {
    id: "bass_drop_hit_01",
    name: "Bass Drop Hit 01",
    path: "assets/01_SFX/03_risers_hits/impact_hits/bass_drop_hit_01.wav",
    file: staticFile("assets/01_SFX/03_risers_hits/impact_hits/bass_drop_hit_01.wav"),
    category: "impacts",
    defaultVolume: 0.40,
  },
  cinematicBoom01: {
    id: "cinematic_boom_01",
    name: "Cinematic Boom 01",
    path: "assets/01_SFX/03_risers_hits/impact_hits/cinematic_boom_01.wav",
    file: staticFile("assets/01_SFX/03_risers_hits/impact_hits/cinematic_boom_01.wav"),
    category: "impacts",
    defaultVolume: 0.42,
  },
  subBassThud: {
    id: "sub_bass_thud",
    name: "Sub Bass Thud",
    path: "assets/01_SFX/03_risers_hits/impact_hits/sub_bass_thud.wav",
    file: staticFile("assets/01_SFX/03_risers_hits/impact_hits/sub_bass_thud.wav"),
    category: "impacts",
    defaultVolume: 0.40,
  },
} as const;

export const SFX_RISERS = {
  metallic01: {
    id: "metallic_riser_01",
    name: "Metallic Riser 01",
    path: "assets/01_SFX/03_risers_hits/metallic_risers/metallic_riser_01.wav",
    file: staticFile("assets/01_SFX/03_risers_hits/metallic_risers/metallic_riser_01.wav"),
    category: "risers",
    defaultVolume: 0.30,
  },
  metallic02: {
    id: "metallic_riser_02",
    name: "Metallic Riser 02",
    path: "assets/01_SFX/03_risers_hits/metallic_risers/metallic_riser_02.wav",
    file: staticFile("assets/01_SFX/03_risers_hits/metallic_risers/metallic_riser_02.wav"),
    category: "risers",
    defaultVolume: 0.30,
  },
  sharpBass01: {
    id: "sharp_bass_riser_01",
    name: "Sharp Bass Riser 01",
    path: "assets/01_SFX/03_risers_hits/sharp_bass_risers/sharp_bass_riser_01.wav",
    file: staticFile("assets/01_SFX/03_risers_hits/sharp_bass_risers/sharp_bass_riser_01.wav"),
    category: "risers",
    defaultVolume: 0.32,
  },
  sharpBass02: {
    id: "sharp_bass_riser_02",
    name: "Sharp Bass Riser 02",
    path: "assets/01_SFX/03_risers_hits/sharp_bass_risers/sharp_bass_riser_02.wav",
    file: staticFile("assets/01_SFX/03_risers_hits/sharp_bass_risers/sharp_bass_riser_02.wav"),
    category: "risers",
    defaultVolume: 0.32,
  },
  sharpBassFast: {
    id: "sharp_bass_riser_fast",
    name: "Sharp Bass Riser Fast",
    path: "assets/01_SFX/03_risers_hits/sharp_bass_risers/sharp_bass_riser_fast.wav",
    file: staticFile("assets/01_SFX/03_risers_hits/sharp_bass_risers/sharp_bass_riser_fast.wav"),
    category: "risers",
    defaultVolume: 0.34,
  },
  riserSubtle: {
    id: "riser_subtle",
    name: "Riser Subtle",
    path: "assets/01_SFX/03_risers_hits/suck_back_risers/riser_subtle.wav",
    file: staticFile("assets/01_SFX/03_risers_hits/suck_back_risers/riser_subtle.wav"),
    category: "risers",
    defaultVolume: 0.28,
  },
  suckBack01: {
    id: "suck_back_riser_01",
    name: "Suck Back Riser 01",
    path: "assets/01_SFX/03_risers_hits/suck_back_risers/suck_back_riser_01.wav",
    file: staticFile("assets/01_SFX/03_risers_hits/suck_back_risers/suck_back_riser_01.wav"),
    category: "risers",
    defaultVolume: 0.30,
  },
  suckBackFast: {
    id: "suck_back_riser_fast",
    name: "Suck Back Riser Fast",
    path: "assets/01_SFX/03_risers_hits/suck_back_risers/suck_back_riser_fast.wav",
    file: staticFile("assets/01_SFX/03_risers_hits/suck_back_risers/suck_back_riser_fast.wav"),
    category: "risers",
    defaultVolume: 0.32,
  },
} as const;

export const SFX_AMBIENCE = {
  techDroneSubtle: {
    id: "tech_drone_subtle",
    name: "Tech Drone Subtle",
    path: "assets/sfx/ambience/tech_drone_subtle.wav",
    file: staticFile("assets/sfx/ambience/tech_drone_subtle.wav"),
    category: "ambience",
    defaultVolume: 0.15,
  },
} as const;

export const ALL_SFX = {
  ...SFX_WHOOSHES,
  ...SFX_TEXTURES,
  ...SFX_POPS,
  ...SFX_SCIFI,
  ...SFX_IMPACTS,
  ...SFX_RISERS,
  ...SFX_AMBIENCE,
} as const;

export type SfxKey = keyof typeof ALL_SFX;

export const FONTS = {
  inter: {
    family: "Inter",
    weights: ["400", "500", "600", "700", "800", "900"],
    regular: staticFile("assets/02_FONTS/01_sans/Inter[opsz,wght].ttf"),
    italic: staticFile("assets/02_FONTS/01_sans/Inter-Italic[opsz,wght].ttf"),
  },
  montserrat: {
    family: "Montserrat",
    weights: ["400", "600", "700", "800", "900"],
    regular: staticFile("assets/02_FONTS/01_sans/Montserrat[wght].ttf"),
    italic: staticFile("assets/02_FONTS/01_sans/Montserrat-Italic[wght].ttf"),
  },
  oswald: {
    family: "Oswald",
    weights: ["400", "600", "700"],
    regular: staticFile("assets/02_FONTS/01_sans/Oswald[wght].ttf"),
  },
  rubik: {
    family: "Rubik",
    weights: ["400", "600", "700", "800", "900"],
    regular: staticFile("assets/02_FONTS/01_sans/Rubik[wght].ttf"),
    italic: staticFile("assets/02_FONTS/01_sans/Rubik-Italic[wght].ttf"),
  },
  unbounded: {
    family: "Unbounded",
    weights: ["400", "700", "900"],
    regular: staticFile("assets/02_FONTS/01_sans/Unbounded[wght].ttf"),
  },
  caveat: {
    family: "Caveat",
    weights: ["700"],
    regular: staticFile("assets/02_FONTS/02_script/Caveat.ttf"),
  },
  segoeScript: {
    family: "Segoe Script",
    weights: ["400", "700"],
    regular: staticFile("assets/02_FONTS/02_script/segoesc.ttf"),
    bold: staticFile("assets/02_FONTS/02_script/segoescb.ttf"),
  },
} as const;

export const GRAPHIC_OVERLAYS = {
  filmGrainLoop: staticFile("assets/03_GRAPHICS/01_overlays/film_grain_35mm_loop.mp4"),
  techGrid: staticFile("assets/03_GRAPHICS/01_overlays/tech_grid_1080x1920.svg"),
} as const;

export const GRAPHIC_BADGES = {
  badgeFact: staticFile("assets/03_GRAPHICS/02_objects_3d/badge_fact.svg"),
  badgeMistake: staticFile("assets/03_GRAPHICS/02_objects_3d/badge_mistake.svg"),
  badgeResult: staticFile("assets/03_GRAPHICS/02_objects_3d/badge_result.svg"),
  calloutArrow: staticFile("assets/03_GRAPHICS/02_objects_3d/callout_arrow.svg"),
  verifiedBadge: staticFile("assets/03_GRAPHICS/02_objects_3d/verified_badge.svg"),
} as const;
