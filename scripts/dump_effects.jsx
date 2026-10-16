(function() {
    var output = [];
    var list = app.effects;
    for (var i = 0; i < list.length; i++) {
        var eff = list[i];
        output.push(eff.displayName + " | " + eff.matchName + " | " + eff.category);
    }
    var scriptFile = new File($.fileName);
    var rootDir = scriptFile.parent.parent;
    var outFile = new File(rootDir.fsName + "/effects_dump.txt");
    outFile.encoding = "UTF-8";
    if (outFile.open("w")) {
        outFile.write(output.join("\n"));
        outFile.close();
        alert("Effects dumped: " + list.length + "\nSaved to: " + outFile.fsName);
    } else {
        var fallbackFile = new File(Folder.desktop.fsName + "/effects_dump.txt");
        fallbackFile.encoding = "UTF-8";
        if (fallbackFile.open("w")) {
            fallbackFile.write(output.join("\n"));
            fallbackFile.close();
            alert("Effects dumped: " + list.length + "\nSaved to desktop: " + fallbackFile.fsName);
        }
    }
})();
