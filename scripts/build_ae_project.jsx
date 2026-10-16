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
            appliedEffect = effectGroup.addProperty(fallbackMatchName);
        } catch (e2) {
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
    app.beginUndoGroup("Build AI Video Project");

    var scriptFile = new File($.fileName);
    var rootFolder = scriptFile.parent.parent;

    var candidatePaths = [
        rootFolder.fsName + "/work/plan/edit_plan.json",
        rootFolder.fsName + "/clients/default/work/plan/edit_plan.json"
    ];

    var jsonFile = null;
    for (var i = 0; i < candidatePaths.length; i++) {
        var testF = new File(candidatePaths[i]);
        if (testF.exists) {
            jsonFile = testF;
            break;
        }
    }

    if (!jsonFile) {
        var selected = File.openDialog("Select edit_plan.json for AE Build", "JSON Files:*.json");
        if (selected && selected.exists) {
            jsonFile = selected;
        }
    }

    if (!jsonFile || !jsonFile.exists) {
        alert("Error: edit_plan.json not found!\nPlease run tools/pipeline.py or select an edit_plan.json file.");
        app.endUndoGroup();
        return;
    }

    jsonFile.encoding = "UTF-8";
    if (!jsonFile.open("r")) {
        alert("Error: Cannot read plan file at: " + jsonFile.fsName);
        app.endUndoGroup();
        return;
    }

    var jsonContent = jsonFile.read();
    jsonFile.close();

    var plan = null;
    try {
        if (typeof JSON !== "undefined" && JSON.parse) {
            plan = JSON.parse(jsonContent);
        } else {
            plan = eval("(" + jsonContent + ")");
        }
    } catch (parseErr) {
        alert("JSON Parse Error in " + jsonFile.name + ": " + parseErr.toString());
        app.endUndoGroup();
        return;
    }

    var compWidth = 1080;
    var compHeight = 1920;
    var compFps = 30;
    var compDuration = plan.target_duration_sec || 15.0;
    var projId = plan.project_id || "Vertical_Reel";
    var compName = projId + "_1080x1920_30fps";

    var comp = app.project.items.addComp(
        compName,
        compWidth,
        compHeight,
        1.0,
        Math.max(1.0, compDuration),
        compFps
    );

    var controlsLayer = comp.layers.addNull();
    controlsLayer.name = "CONTROLS";
    controlsLayer.label = 1;

    var colorFx = safeApplyEffect(controlsLayer, "ADBE Color Control", null, {});
    if (colorFx && colorFx.property("ADBE Color Control-0001")) {
        colorFx.name = "Accent Color";
        colorFx.property("ADBE Color Control-0001").setValue([1.0, 0.84, 0.04, 1.0]);
    }

    var shadowFx = safeApplyEffect(controlsLayer, "ADBE Slider Control", null, {});
    if (shadowFx && shadowFx.property("ADBE Slider Control-0001")) {
        shadowFx.name = "Shadow Opacity";
        shadowFx.property("ADBE Slider Control-0001").setValue(40);
    }

    var roundnessFx = safeApplyEffect(controlsLayer, "ADBE Slider Control", null, {});
    if (roundnessFx && roundnessFx.property("ADBE Slider Control-0001")) {
        roundnessFx.name = "Card Roundness";
        roundnessFx.property("ADBE Slider Control-0001").setValue(24);
    }

    var sdrPath = plan.sdr_path || plan.proxy_path;
    var videoLayer = null;
    if (sdrPath) {
        var vFile = new File(sdrPath);
        if (!vFile.exists) {
            vFile = new File(rootFolder.fsName + "/" + sdrPath.replace(/\\/g, "/"));
        }
        if (vFile.exists) {
            try {
                var vOpts = new ImportOptions(vFile);
                var vItem = app.project.importFile(vOpts);
                videoLayer = comp.layers.add(vItem);
                videoLayer.name = "SDR_Speaker_Footage";
                videoLayer.label = 9;
                videoLayer.moveToEnd();

                if (vItem.width > vItem.height) {
                    var scaleFactor = (compHeight / vItem.height) * 100;
                    videoLayer.property("ADBE Transform Group").property("ADBE Scale").setValue([scaleFactor, scaleFactor, 100]);
                    videoLayer.property("ADBE Transform Group").property("ADBE Position").setValue([compWidth / 2, compHeight / 2]);
                }
            } catch (vErr) {
                $.writeln("Video footage import failed: " + vErr.toString());
            }
        }
    }

    var beats = plan.beats || [];
    for (var b = 0; b < beats.length; b++) {
        var beat = beats[b];
        var tRange = beat.time_range || [0.0, 3.0];
        var bStart = tRange[0];
        var bEnd = tRange[1];
        var bDur = Math.max(0.1, bEnd - bStart);

        if (beat.line && beat.line !== "") {
            var textLayer = comp.layers.addText(beat.line);
            textLayer.name = "Caption_Beat_" + (beat.beat_index !== undefined ? beat.beat_index : b);
            textLayer.label = 13;
            textLayer.startTime = bStart;
            textLayer.inPoint = bStart;
            textLayer.outPoint = bEnd;

            var textProp = textLayer.property("ADBE Text Properties").property("ADBE Text Document");
            var textDoc = textProp.value;
            textDoc.fontSize = 54;
            textDoc.fillColor = [1, 1, 1];
            textDoc.font = "Montserrat-ExtraBold";
            textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
            textProp.setValue(textDoc);

            var posProp = textLayer.property("ADBE Transform Group").property("ADBE Position");
            posProp.setValue([compWidth / 2, 1250]);

            var scaleProp = textLayer.property("ADBE Transform Group").property("ADBE Scale");
            scaleProp.setValueAtTime(bStart, [85, 85, 100]);
            scaleProp.setValueAtTime(bStart + 0.15, [104, 104, 100]);
            scaleProp.setValueAtTime(bStart + 0.30, [100, 100, 100]);

            var opacProp = textLayer.property("ADBE Transform Group").property("ADBE Opacity");
            opacProp.setValueAtTime(bStart, 0);
            opacProp.setValueAtTime(bStart + 0.10, 100);

            safeApplyEffect(textLayer, "ADBE Drop Shadow", null, {
                "ADBE Drop Shadow-0001": [0, 0, 0, 1],
                "ADBE Drop Shadow-0002": 180,
                "ADBE Drop Shadow-0003": 8,
                "ADBE Drop Shadow-0004": 15
            });
        }

        if (beat.proof_source && beat.proof_source !== "") {
            var pFile = new File(beat.proof_source);
            if (!pFile.exists) {
                pFile = new File(rootFolder.fsName + "/" + beat.proof_source.replace(/\\/g, "/"));
            }
            if (pFile.exists) {
                try {
                    var pOpts = new ImportOptions(pFile);
                    var pItem = app.project.importFile(pOpts);
                    var proofLayer = comp.layers.add(pItem);
                    proofLayer.name = "Proof_Badge_Beat_" + b;
                    proofLayer.label = 11;
                    proofLayer.startTime = bStart;
                    proofLayer.inPoint = bStart;
                    proofLayer.outPoint = bEnd;
                    proofLayer.property("ADBE Transform Group").property("ADBE Position").setValue([compWidth / 2, 600]);

                    var pScale = proofLayer.property("ADBE Transform Group").property("ADBE Scale");
                    pScale.setValueAtTime(bStart, [70, 70, 100]);
                    pScale.setValueAtTime(bStart + 0.20, [103, 103, 100]);
                    pScale.setValueAtTime(bStart + 0.35, [100, 100, 100]);

                    safeApplyEffect(proofLayer, "ADBE Drop Shadow", null, {
                        "ADBE Drop Shadow-0002": 150,
                        "ADBE Drop Shadow-0003": 12,
                        "ADBE Drop Shadow-0004": 30
                    });
                } catch (pErr) {
                    $.writeln("Proof asset import failed: " + pErr.toString());
                }
            }
        }

        if (beat.sfx && beat.sfx !== "" && beat.sfx !== "TODO" && beat.sfx !== "none") {
            var relSfx = beat.sfx.replace(/^assets\/sfx\//, "").replace(/^sfx\//, "");
            var sFile = new File(rootFolder.fsName + "/assets/sfx/" + relSfx + (relSfx.indexOf(".wav") === -1 ? ".wav" : ""));
            if (sFile.exists) {
                try {
                    var sOpts = new ImportOptions(sFile);
                    var sItem = app.project.importFile(sOpts);
                    var sLayer = comp.layers.add(sItem);
                    sLayer.name = "SFX_Beat_" + b;
                    sLayer.label = 7;
                    sLayer.startTime = bStart;
                    sLayer.inPoint = bStart;
                    sLayer.outPoint = Math.min(compDuration, bStart + 2.0);
                } catch (sErr) {
                }
            }
        }
    }

    var grainLayer = comp.layers.addSolid([1, 1, 1], "Master_AntiSlop_Grain", compWidth, compHeight, 1.0, compDuration);
    grainLayer.adjustmentLayer = true;
    grainLayer.label = 8;
    safeApplyEffect(grainLayer, "ADBE Noise2", null, {
        "ADBE Noise2-0001": 3.0,
        "ADBE Noise2-0002": 0
    });

    app.endUndoGroup();
    alert("After Effects Project Assembled Successfully!\nComposition: " + compName + "\nDuration: " + compDuration + "s @ 30 fps\nBeats processed: " + beats.length);
})();
