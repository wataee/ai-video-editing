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
    path: "assets/sfx/whooshes/deep_voice_whoosh_01.wav",
    file: staticFile("sfx/whooshes/deep_voice_whoosh_01.wav"),
    category: "whooshes",
    defaultVolume: 0.10,
  },
  deepVoice02: {
    id: "deep_voice_whoosh_02",
    name: "Deep Voice Whoosh 02",
    path: "assets/sfx/whooshes/deep_voice_whoosh_02.wav",
    file: staticFile("sfx/whooshes/deep_voice_whoosh_02.wav"),
    category: "whooshes",
    defaultVolume: 0.10,
  },
  deepVoice03: {
    id: "deep_voice_whoosh_03",
    name: "Deep Voice Whoosh 03",
    path: "assets/sfx/whooshes/deep_voice_whoosh_03.wav",
    file: staticFile("sfx/whooshes/deep_voice_whoosh_03.wav"),
    category: "whooshes",
    defaultVolume: 0.10,
  },
  cleanFast: {
    id: "whoosh_clean_fast",
    name: "Whoosh Clean Fast",
    path: "assets/sfx/whooshes/whoosh_clean_fast.wav",
    file: staticFile("sfx/whooshes/whoosh_clean_fast.wav"),
    category: "whooshes",
    defaultVolume: 0.10,
  },
  hollow01: {
    id: "hollow_whoosh_01",
    name: "Hollow Whoosh 01",
    path: "assets/sfx/whooshes/hollow_whoosh_01.wav",
    file: staticFile("sfx/whooshes/hollow_whoosh_01.wav"),
    category: "whooshes",
    defaultVolume: 0.10,
  },
  hollow02: {
    id: "hollow_whoosh_02",
    name: "Hollow Whoosh 02",
    path: "assets/sfx/whooshes/hollow_whoosh_02.wav",
    file: staticFile("sfx/whooshes/hollow_whoosh_02.wav"),
    category: "whooshes",
    defaultVolume: 0.10,
  },
  subtleAir: {
    id: "whoosh_subtle_air",
    name: "Whoosh Subtle Air",
    path: "assets/sfx/whooshes/whoosh_subtle_air.wav",
    file: staticFile("sfx/whooshes/whoosh_subtle_air.wav"),
    category: "whooshes",
    defaultVolume: 0.10,
  },
  syntheticTransition: {
    id: "synthetic_transition_whoosh",
    name: "Synthetic Transition Whoosh",
    path: "assets/sfx/whooshes/synthetic_transition_whoosh.wav",
    file: staticFile("sfx/whooshes/synthetic_transition_whoosh.wav"),
    category: "whooshes",
    defaultVolume: 0.10,
  },
  transitionSpacey: {
    id: "transition_spacey_whoosh",
    name: "Transition Spacey Whoosh",
    path: "assets/sfx/whooshes/transition_spacey_whoosh.wav",
    file: staticFile("sfx/whooshes/transition_spacey_whoosh.wav"),
    category: "whooshes",
    defaultVolume: 0.10,
  },
} as const;

export const SFX_TEXTURES = {
  cameraClickFast: {
    id: "camera_click_fast",
    name: "Camera Click Fast",
    path: "assets/sfx/textures/camera_click_fast.wav",
    file: staticFile("sfx/textures/camera_click_fast.wav"),
    category: "textures",
    defaultVolume: 0.15,
  },
  click01: {
    id: "click_01",
    name: "Click 01",
    path: "assets/sfx/clicks/click_01.wav",
    file: staticFile("sfx/clicks/click_01.wav"),
    category: "textures",
    defaultVolume: 0.15,
  },
  click02: {
    id: "click_02",
    name: "Click 02",
    path: "assets/sfx/clicks/click_02.wav",
    file: staticFile("sfx/clicks/click_02.wav"),
    category: "textures",
    defaultVolume: 0.15,
  },
  mechanicalButton: {
    id: "mechanical_button",
    name: "Mechanical Button",
    path: "assets/sfx/clicks/mechanical_button.wav",
    file: staticFile("sfx/clicks/mechanical_button.wav"),
    category: "textures",
    defaultVolume: 0.15,
  },
  mouseClickSoft: {
    id: "mouse_click_soft",
    name: "Mouse Click Soft",
    path: "assets/sfx/clicks/mouse_click_soft.wav",
    file: staticFile("sfx/clicks/mouse_click_soft.wav"),
    category: "textures",
    defaultVolume: 0.15,
  },
  select01: {
    id: "select_01",
    name: "Select 01",
    path: "assets/sfx/clicks/select_01.wav",
    file: staticFile("sfx/clicks/select_01.wav"),
    category: "textures",
    defaultVolume: 0.15,
  },
  switch01: {
    id: "switch_01",
    name: "Switch 01",
    path: "assets/sfx/clicks/switch_01.wav",
    file: staticFile("sfx/clicks/switch_01.wav"),
    category: "textures",
    defaultVolume: 0.15,
  },
  complexGizmo: {
    id: "complex_mechanism_gizmo",
    name: "Complex Mechanism Gizmo",
    path: "assets/sfx/textures/complex_mechanism_gizmo.wav",
    file: staticFile("sfx/textures/complex_mechanism_gizmo.wav"),
    category: "textures",
    defaultVolume: 0.15,
  },
  scratch01: {
    id: "scratch_01",
    name: "Scratch 01",
    path: "assets/sfx/textures/scratch_01.wav",
    file: staticFile("sfx/textures/scratch_01.wav"),
    category: "textures",
    defaultVolume: 0.15,
  },
  scratch02: {
    id: "scratch_02",
    name: "Scratch 02",
    path: "assets/sfx/textures/scratch_02.wav",
    file: staticFile("sfx/textures/scratch_02.wav"),
    category: "textures",
    defaultVolume: 0.15,
  },
  tinyGearwheelLoop: {
    id: "tiny_gearwheel_loop",
    name: "Tiny Gearwheel Loop",
    path: "assets/sfx/textures/tiny_gearwheel_loop.wav",
    file: staticFile("sfx/textures/tiny_gearwheel_loop.wav"),
    category: "textures",
    defaultVolume: 0.12,
  },
} as const;

export const SFX_POPS = {
  glassPop: {
    id: "glass_pop",
    name: "Glass Pop",
    path: "assets/sfx/pops/glass_pop.wav",
    file: staticFile("sfx/pops/glass_pop.wav"),
    category: "pops",
    defaultVolume: 0.15,
  },
  pop01: {
    id: "pop_01",
    name: "Pop 01",
    path: "assets/sfx/pops/pop_01.wav",
    file: staticFile("sfx/pops/pop_01.wav"),
    category: "pops",
    defaultVolume: 0.15,
  },
  pop02: {
    id: "pop_02",
    name: "Pop 02",
    path: "assets/sfx/pops/pop_02.wav",
    file: staticFile("sfx/pops/pop_02.wav"),
    category: "pops",
    defaultVolume: 0.15,
  },
  popBubbleHigh: {
    id: "pop_bubble_high",
    name: "Pop Bubble High",
    path: "assets/sfx/pops/pop_bubble_high.wav",
    file: staticFile("sfx/pops/pop_bubble_high.wav"),
    category: "pops",
    defaultVolume: 0.15,
  },
  popCartoonClean: {
    id: "pop_cartoon_clean",
    name: "Pop Cartoon Clean",
    path: "assets/sfx/pops/pop_cartoon_clean.wav",
    file: staticFile("sfx/pops/pop_cartoon_clean.wav"),
    category: "pops",
    defaultVolume: 0.15,
  },
} as const;

export const SFX_SCIFI = {
  activateEnergyHit: {
    id: "activate_energy_hit",
    name: "Activate Energy Hit",
    path: "assets/sfx/glitches/activate_energy_hit.wav",
    file: staticFile("sfx/glitches/activate_energy_hit.wav"),
    category: "sciFi",
    defaultVolume: 0.15,
  },
  glitch01: {
    id: "glitch_01",
    name: "Glitch 01",
    path: "assets/sfx/glitches/glitch_01.wav",
    file: staticFile("sfx/glitches/glitch_01.wav"),
    category: "sciFi",
    defaultVolume: 0.15,
  },
  glitch02: {
    id: "glitch_02",
    name: "Glitch 02",
    path: "assets/sfx/glitches/glitch_02.wav",
    file: staticFile("sfx/glitches/glitch_02.wav"),
    category: "sciFi",
    defaultVolume: 0.15,
  },
  sciFiImpactReveal: {
    id: "sci_fi_impact_reveal",
    name: "Sci-Fi Impact Reveal",
    path: "assets/sfx/glitches/sci_fi_impact_reveal.wav",
    file: staticFile("sfx/glitches/sci_fi_impact_reveal.wav"),
    category: "sciFi",
    defaultVolume: 0.15,
  },
} as const;

export const SFX_IMPACTS = {
  bassDrop01: {
    id: "bass_drop_hit_01",
    name: "Bass Drop Hit 01",
    path: "assets/sfx/hits/bass_drop_hit_01.wav",
    file: staticFile("sfx/hits/bass_drop_hit_01.wav"),
    category: "impacts",
    defaultVolume: 0.20,
  },
  cinematicBoom01: {
    id: "cinematic_boom_01",
    name: "Cinematic Boom 01",
    path: "assets/sfx/hits/cinematic_boom_01.wav",
    file: staticFile("sfx/hits/cinematic_boom_01.wav"),
    category: "impacts",
    defaultVolume: 0.20,
  },
  subBassThud: {
    id: "sub_bass_thud",
    name: "Sub Bass Thud",
    path: "assets/sfx/hits/sub_bass_thud.wav",
    file: staticFile("sfx/hits/sub_bass_thud.wav"),
    category: "impacts",
    defaultVolume: 0.20,
  },
} as const;

export const SFX_RISERS = {
  metallic01: {
    id: "metallic_riser_01",
    name: "Metallic Riser 01",
    path: "assets/sfx/risers/metallic_riser_01.wav",
    file: staticFile("sfx/risers/metallic_riser_01.wav"),
    category: "risers",
    defaultVolume: 0.20,
  },
  metallic02: {
    id: "metallic_riser_02",
    name: "Metallic Riser 02",
    path: "assets/sfx/risers/metallic_riser_02.wav",
    file: staticFile("sfx/risers/metallic_riser_02.wav"),
    category: "risers",
    defaultVolume: 0.20,
  },
  sharpBass01: {
    id: "sharp_bass_riser_01",
    name: "Sharp Bass Riser 01",
    path: "assets/sfx/risers/sharp_bass_riser_01.wav",
    file: staticFile("sfx/risers/sharp_bass_riser_01.wav"),
    category: "risers",
    defaultVolume: 0.20,
  },
  sharpBass02: {
    id: "sharp_bass_riser_02",
    name: "Sharp Bass Riser 02",
    path: "assets/sfx/risers/sharp_bass_riser_02.wav",
    file: staticFile("sfx/risers/sharp_bass_riser_02.wav"),
    category: "risers",
    defaultVolume: 0.20,
  },
  sharpBassFast: {
    id: "sharp_bass_riser_fast",
    name: "Sharp Bass Riser Fast",
    path: "assets/sfx/risers/sharp_bass_riser_fast.wav",
    file: staticFile("sfx/risers/sharp_bass_riser_fast.wav"),
    category: "risers",
    defaultVolume: 0.20,
  },
  riserSubtle: {
    id: "riser_subtle",
    name: "Riser Subtle",
    path: "assets/sfx/risers/riser_subtle.wav",
    file: staticFile("sfx/risers/riser_subtle.wav"),
    category: "risers",
    defaultVolume: 0.20,
  },
  suckBack01: {
    id: "suck_back_riser_01",
    name: "Suck Back Riser 01",
    path: "assets/sfx/risers/suck_back_riser_01.wav",
    file: staticFile("sfx/risers/suck_back_riser_01.wav"),
    category: "risers",
    defaultVolume: 0.20,
  },
  suckBackFast: {
    id: "suck_back_riser_fast",
    name: "Suck Back Riser Fast",
    path: "assets/sfx/risers/suck_back_riser_fast.wav",
    file: staticFile("sfx/risers/suck_back_riser_fast.wav"),
    category: "risers",
    defaultVolume: 0.20,
  },
} as const;

export const SFX_AMBIENCE = {
  techDroneSubtle: {
    id: "tech_drone_subtle",
    name: "Tech Drone Subtle",
    path: "assets/sfx/ambience/tech_drone_subtle.wav",
    file: staticFile("sfx/ambience/tech_drone_subtle.wav"),
    category: "ambience",
    defaultVolume: 0.08,
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
    regular: staticFile("fonts/Inter/Inter[opsz,wght].ttf"),
    italic: staticFile("fonts/Inter/Inter-Italic[opsz,wght].ttf"),
  },
  manrope: {
    family: "Manrope",
    weights: ["400", "500", "600", "700", "800"],
    regular: staticFile("fonts/Manrope/Manrope[wght].ttf"),
  },
  montserrat: {
    family: "Montserrat",
    weights: ["400", "600", "700", "800", "900"],
    regular: staticFile("fonts/Montserrat/Montserrat[wght].ttf"),
    italic: staticFile("fonts/Montserrat/Montserrat-Italic[wght].ttf"),
  },
  oswald: {
    family: "Oswald",
    weights: ["400", "600", "700"],
    regular: staticFile("fonts/Oswald/Oswald[wght].ttf"),
  },
  rubik: {
    family: "Rubik",
    weights: ["400", "600", "700", "800", "900"],
    regular: staticFile("fonts/Rubik/Rubik[wght].ttf"),
    italic: staticFile("fonts/Rubik/Rubik-Italic[wght].ttf"),
  },
  unbounded: {
    family: "Unbounded",
    weights: ["400", "700", "900"],
    regular: staticFile("fonts/Unbounded/Unbounded[wght].ttf"),
  },
  caveat: {
    family: "Caveat",
    weights: ["700"],
    regular: staticFile("fonts/Caveat/Caveat.ttf"),
  },
} as const;

export const GRAPHIC_OVERLAYS = {
  filmGrainLoop: staticFile("overlays/film_grain/film_grain_35mm_loop.mp4"),
  techGrid: staticFile("overlays/grids/tech_grid_1080x1920.svg"),
} as const;

export const GRAPHIC_BADGES = {
  badgeFact: staticFile("ui/badges/badge_fact.svg"),
  badgeMistake: staticFile("ui/badges/badge_mistake.svg"),
  badgeResult: staticFile("ui/badges/badge_result.svg"),
  calloutArrow: staticFile("ui/arrows/callout_arrow.svg"),
  verifiedBadge: staticFile("ui/badges/verified_badge.svg"),
} as const;
