const code = document.getElementById('editor');


const editor = monaco.editor.create(code, {
    value: "",
    language: "python",
});

editor.setValue("print('Hello, World!')");

monaco.editor.setTheme('vs-dark');