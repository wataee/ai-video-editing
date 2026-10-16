function safeApplyEffect(layer, primaryMatchName, fallbackMatchName, params) {
    if (!layer || !layer.property) {
        return null;
    }
    var effectGroup = layer.property("ADBE Effect Parade");
    if (!effectGroup) {
        return null;
    }
    var appliedEffect = null;
    if (primaryMatchName && primaryMatchName !== "") {
        try {
            appliedEffect = effectGroup.addProperty(primaryMatchName);
        } catch (e) {
            appliedEffect = null;
        }
    }
    if (!appliedEffect && fallbackMatchName && fallbackMatchName !== "") {
        try {
            $.writeln("[safeApplyEffect] Falling back from " + primaryMatchName + " to " + fallbackMatchName);
            appliedEffect = effectGroup.addProperty(fallbackMatchName);
        } catch (e2) {
            $.writeln("[safeApplyEffect Error] Failed fallback " + fallbackMatchName + ": " + e2.toString());
            appliedEffect = null;
        }
    }
    if (appliedEffect && params) {
        for (var key in params) {
            if (params.hasOwnProperty(key)) {
                try {
                    var prop = appliedEffect.property(key);
                    if (prop && prop.setValue) {
                        prop.setValue(params[key]);
                    }
                } catch (paramErr) {
                }
            }
        }
    }
    return appliedEffect;
}

(function () {
    app.beginUndoGroup("AI Video Build");

    var scriptFile = new File($.fileName);
    var rootFolder = scriptFile.parent.parent;
    var jsonFile = new File(rootFolder.fsName + "/src/data/beat_sheet.json");

    if (!jsonFile.exists) {
        alert("File not found: " + jsonFile.fsName);
        app.endUndoGroup();
        return;
    }

    jsonFile.encoding = "UTF-8";
    if (!jsonFile.open("r")) {
        alert("Failed to open: " + jsonFile.fsName);
        app.endUndoGroup();
        return;
    }

    var jsonContent = jsonFile.read();
    jsonFile.close();

    var data = null;
    try {
        if (typeof JSON !== "undefined" && JSON.parse) {
            data = JSON.parse(jsonContent);
        } else {
            data = eval("(" + jsonContent + ")");
        }
    } catch (parseErr) {
        alert("JSON parse error: " + parseErr.toString());
        app.endUndoGroup();
        return;
    }

    var compWidth = data.width || 1080;
    var compHeight = data.height || 1920;
    var compFps = data.fps || 60;
    var compDuration = data.target_duration_sec || 10;
    var compName = data.title || "AI_Video_Master";

    var comp = app.project.items.addComp(
        compName,
        compWidth,
        compHeight,
        1.0,
        compDuration,
        compFps
    );

    for (var s = 0; s < data.scenes.length; s++) {
        var sceneItem = data.scenes[s];
        var stemFileName = rootFolder.fsName + "/out/stems/" + sceneItem.id + "_ui.mov";
        var stemFile = new File(stemFileName);
        if (!stemFile.exists) {
            stemFileName = rootFolder.fsName + "/out/stems/scene_0" + (s + 1) + "_ui.mov";
            stemFile = new File(stemFileName);
        }
        if (stemFile.exists) {
            try {
                var importOpts = new ImportOptions(stemFile);
                var footage = app.project.importFile(importOpts);
                var layer = comp.layers.add(footage);
                layer.startTime = sceneItem.start_frame / compFps;
                layer.inPoint = sceneItem.start_frame / compFps;
                layer.outPoint = (sceneItem.start_frame + sceneItem.duration_in_frames) / compFps;
                layer.name = "Stem_" + sceneItem.name;
            } catch (stemErr) {
                $.writeln("[Stem Import Warning] " + stemErr.toString());
            }
        }
    }

    for (var t = 0; t < data.scenes.length; t++) {
        var sc = data.scenes[t];
        if (sc.title) {
            var textLayer = comp.layers.addText(sc.title);
            textLayer.name = "Text_" + sc.name;
            textLayer.startTime = sc.start_frame / compFps;
            textLayer.inPoint = sc.start_frame / compFps;
            textLayer.outPoint = (sc.start_frame + sc.duration_in_frames) / compFps;

            var textProp = textLayer.property("ADBE Text Properties").property("ADBE Text Document");
            var textDoc = textProp.value;
            textDoc.fontSize = 56;
            textDoc.fillColor = [1, 1, 1];
            textDoc.font = "Montserrat-ExtraBold";
            textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
            textProp.setValue(textDoc);

            var posProp = textLayer.property("ADBE Transform Group").property("ADBE Position");
            posProp.setValue([compWidth / 2, compHeight * 0.28]);

            var scaleProp = textLayer.property("ADBE Transform Group").property("ADBE Scale");
            var tStart = sc.start_frame / compFps;
            scaleProp.setValueAtTime(tStart, [85, 85, 100]);
            scaleProp.setValueAtTime(tStart + 0.25, [103, 103, 100]);
            scaleProp.setValueAtTime(tStart + 0.45, [100, 100, 100]);

            var opacityProp = textLayer.property("ADBE Transform Group").property("ADBE Opacity");
            opacityProp.setValueAtTime(tStart, 0);
            opacityProp.setValueAtTime(tStart + 0.15, 100);
        }
    }

    for (var a = 0; a < data.scenes.length; a++) {
        var curScene = data.scenes[a];
        if (curScene.sfx && curScene.sfx.sample) {
            var relSample = curScene.sfx.sample.replace("assets/01_SFX/", "").replace("assets/sfx/", "");
            var sfxFile = new File(rootFolder.fsName + "/assets/01_SFX/" + relSample);
            if (!sfxFile.exists) {
                sfxFile = new File(rootFolder.fsName + "/assets/sfx/" + relSample);
            }
            if (sfxFile.exists) {
                try {
                    var audioOpts = new ImportOptions(sfxFile);
                    var audioItem = app.project.importFile(audioOpts);
                    var audioLayer = comp.layers.add(audioItem);
                    var audioStartSec = (curScene.start_frame + (curScene.sfx.frame_offset || 0)) / compFps;
                    audioLayer.startTime = audioStartSec;
                    audioLayer.name = "SFX_" + curScene.name;
                    var audioLevels = audioLayer.property("ADBE Audio Group").property("ADBE Audio Levels");
                    if (audioLevels) {
                        var vol = curScene.sfx.volume_db || -14;
                        audioLevels.setValue([vol, vol]);
                    }
                } catch (audioErr) {
                    $.writeln("[SFX Import Warning] " + audioErr.toString());
                }
            }
        }
    }

    var adjLayer = comp.layers.addSolid([1, 1, 1], "Adjustment_Master_Grade", compWidth, compHeight, 1.0, compDuration);
    adjLayer.adjustmentLayer = true;

    safeApplyEffect(adjLayer, "VIDEOCOPILOT OpticalGlow", "ADBE Glo2", {
        "ADBE Glo2-0001": 55,
        "ADBE Glo2-0002": 25,
        "ADBE Glo2-0003": 0.8
    });

    safeApplyEffect(adjLayer, "REVision Plug-ins RSMB", "ADBE Motion Blur", {
        "ADBE Motion Blur-0001": 0,
        "ADBE Motion Blur-0002": 8
    });

    safeApplyEffect(adjLayer, "ADBE Noise2", null, {
        "ADBE Noise2-0001": 3.5,
        "ADBE Noise2-0002": 0
    });

    safeApplyEffect(adjLayer, "ADBE Optics Compensation", null, {
        "ADBE Optics Compensation-0001": 12,
        "ADBE Optics Compensation-0002": 1
    });

    app.endUndoGroup();
    alert("AI Video Build complete!\nCreated: " + compName + " (" + compWidth + "x" + compHeight + " @ " + compFps + " fps)");
})();
