
function createCalloutBox(comp, textString, badgeString, inTimeSec, durationSec) {
    app.beginUndoGroup("Create Pro Callout Card");
    try {
        if (!comp) comp = app.project.activeItem;
        if (!comp || !(comp instanceof CompItem)) return;

        var textLayer = comp.layers.addText(textString);
        textLayer.startTime = inTimeSec;
        textLayer.inPoint = inTimeSec;
        textLayer.outPoint = inTimeSec + durationSec;
        
        var textProp = textLayer.property("Source Text");
        var textDoc = textProp.value;
        textDoc.fontSize = 54;
        textDoc.fillColor = [1, 1, 1];
        textDoc.font = "Inter-Bold";
        textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
        textProp.setValue(textDoc);

        textLayer.property("Position").setValue([comp.width / 2, comp.height * 0.65]);

        var shapeLayer = comp.layers.addShape();
        shapeLayer.name = "Callout_Background";
        shapeLayer.moveAfter(textLayer);
        shapeLayer.startTime = inTimeSec;
        shapeLayer.inPoint = inTimeSec;
        shapeLayer.outPoint = inTimeSec + durationSec;

        var scaleProp = textLayer.property("Scale");
        scaleProp.setValueAtTime(inTimeSec, [85, 85]);
        scaleProp.setValueAtTime(inTimeSec + 0.15, [105, 105]);
        scaleProp.setValueAtTime(inTimeSec + 0.25, [100, 100]);
        
    } finally {
        app.endUndoGroup();
    }
}
