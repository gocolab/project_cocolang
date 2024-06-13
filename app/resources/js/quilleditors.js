// common.js

document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('#description_delta')) {
        let quillSettings = { theme: 'snow' };
        let quillDescription = new Quill('#description_delta', quillSettings);
        let deltaObject = JSON.parse(document.querySelector('#description_delta').dataset.delta);
        quillDescription.setContents(deltaObject);

        document.querySelector('form').onsubmit = function (event) {
            document.querySelector('#description').value = JSON.stringify(quillDescription.getContents());
        };
    }

});
