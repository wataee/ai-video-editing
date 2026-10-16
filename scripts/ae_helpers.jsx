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

function safeFindComp(compName) {
    if (!app.project) {
        return null;
    }
    for (var i = 1; i <= app.project.numItems; i++) {
        var item = app.project.item(i);
        if (item instanceof CompItem && item.name === compName) {
            return item;
        }
    }
    return null;
}

function safeImportFootage(filePath) {
    var fileObj = new File(filePath);
    if (!fileObj.exists) {
        $.writeln("[safeImportFootage] File not found: " + filePath);
        return null;
    }
    try {
        var importOptions = new ImportOptions(fileObj);
        return app.project.importFile(importOptions);
    } catch (e) {
        $.writeln("[safeImportFootage Error] " + e.toString());
        return null;
    }
}

function safeAddAdjustmentLayer(comp, layerName, durationSec) {
    if (!comp) {
        return null;
    }
    var adjLayer = comp.layers.addSolid([1, 1, 1], layerName, comp.width, comp.height, comp.pixelAspect, durationSec || comp.duration);
    adjLayer.adjustmentLayer = true;
    return adjLayer;
}
