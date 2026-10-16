import { Config } from "@remotion/cli/config";

Config.setRspack(true);
Config.setPublicDir("assets");
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
Config.setChromiumOpenGlRenderer("angle");
Config.setPixelFormat("yuv420p");
