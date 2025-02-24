document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll("pre").forEach((pre) => {
        if (pre.parentNode.classList.contains("code-wrapper")) return;

        const wrapper = document.createElement("div");
        wrapper.classList.add("code-wrapper");
        pre.parentNode.insertBefore(wrapper, pre);
        wrapper.appendChild(pre);

        const button = document.createElement("button");
        button.classList.add("copy-button");
        // Fluent Clipboard Code Regular, MIT License
        button.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><path fill="currentColor" d="M7.085 3A1.5 1.5 0 0 1 8.5 2h3a1.5 1.5 0 0 1 1.415 1H14.5A1.5 1.5 0 0 1 16 4.5v5.877A1.5 1.5 0 0 0 15 10V4.5a.5.5 0 0 0-.5-.5h-1.585A1.5 1.5 0 0 1 11.5 5h-3a1.5 1.5 0 0 1-1.415-1H5.5a.5.5 0 0 0-.5.5v12a.5.5 0 0 0 .5.5h3.957l.404.472a1.5 1.5 0 0 0 1.139.524V18H5.5A1.5 1.5 0 0 1 4 16.5v-12A1.5 1.5 0 0 1 5.5 3zM8.5 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm6.986 8.638a.5.5 0 1 0-.962-.275l-2 7a.5.5 0 1 0 .962.274zM11.38 13.32a.5.5 0 1 0-.76-.65l-1.5 1.75a.5.5 0 0 0 0 .65l1.5 1.75a.5.5 0 1 0 .76-.65l-1.222-1.425zm5.295 3.554a.5.5 0 0 1-.055-.705l1.221-1.424l-1.22-1.425a.5.5 0 0 1 .759-.65l1.5 1.75a.5.5 0 0 1 0 .65l-1.5 1.75a.5.5 0 0 1-.705.054"/></svg>
                 `;

        wrapper.appendChild(button);

        button.addEventListener("click", () => {
            navigator.clipboard
                .writeText(pre.innerText)
                .then(() => {
                    // Fluent Icon Task, MIT License
                    button.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><path fill="currentColor" d="M12.854 9.854a.5.5 0 0 0-.708-.708L9 12.293l-1.146-1.147a.5.5 0 0 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0zM8.5 2a1.5 1.5 0 0 0-1.415 1H5.5A1.5 1.5 0 0 0 4 4.5v12A1.5 1.5 0 0 0 5.5 18h9a1.5 1.5 0 0 0 1.5-1.5v-12A1.5 1.5 0 0 0 14.5 3h-1.585A1.5 1.5 0 0 0 11.5 2zM8 3.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5M5.5 4h1.585A1.5 1.5 0 0 0 8.5 5h3a1.5 1.5 0 0 0 1.415-1H14.5a.5.5 0 0 1 .5.5v12a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5v-12a.5.5 0 0 1 .5-.5"/></svg>
                                              `;
                    setTimeout(() => {
                        button.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><path fill="currentColor" d="M7.085 3A1.5 1.5 0 0 1 8.5 2h3a1.5 1.5 0 0 1 1.415 1H14.5A1.5 1.5 0 0 1 16 4.5v5.877A1.5 1.5 0 0 0 15 10V4.5a.5.5 0 0 0-.5-.5h-1.585A1.5 1.5 0 0 1 11.5 5h-3a1.5 1.5 0 0 1-1.415-1H5.5a.5.5 0 0 0-.5.5v12a.5.5 0 0 0 .5.5h3.957l.404.472a1.5 1.5 0 0 0 1.139.524V18H5.5A1.5 1.5 0 0 1 4 16.5v-12A1.5 1.5 0 0 1 5.5 3zM8.5 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zm6.986 8.638a.5.5 0 1 0-.962-.275l-2 7a.5.5 0 1 0 .962.274zM11.38 13.32a.5.5 0 1 0-.76-.65l-1.5 1.75a.5.5 0 0 0 0 .65l1.5 1.75a.5.5 0 1 0 .76-.65l-1.222-1.425zm5.295 3.554a.5.5 0 0 1-.055-.705l1.221-1.424l-1.22-1.425a.5.5 0 0 1 .759-.65l1.5 1.75a.5.5 0 0 1 0 .65l-1.5 1.75a.5.5 0 0 1-.705.054"/></svg>
                 `;
                    }, 2000);
                })
                .catch(() => {
                    // Fluent Icon Error Clipboard, MIT License
                    button.innerHTML = `
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20"><path fill="currentColor" d="M7.085 3A1.5 1.5 0 0 1 8.5 2h3a1.5 1.5 0 0 1 1.415 1H14.5A1.5 1.5 0 0 1 16 4.5v4.707a5.5 5.5 0 0 0-1-.185V4.5a.5.5 0 0 0-.5-.5h-1.585A1.5 1.5 0 0 1 11.5 5h-3a1.5 1.5 0 0 1-1.415-1H5.5a.5.5 0 0 0-.5.5v12a.5.5 0 0 0 .5.5h4.1q.276.538.657 1H5.5A1.5 1.5 0 0 1 4 16.5v-12A1.5 1.5 0 0 1 5.5 3zM8.5 3a.5.5 0 0 0 0 1h3a.5.5 0 0 0 0-1zM19 14.5a4.5 4.5 0 1 1-9 0a4.5 4.5 0 0 1 9 0M14.5 12a.5.5 0 0 0-.5.5v2a.5.5 0 0 0 1 0v-2a.5.5 0 0 0-.5-.5m0 5.125a.625.625 0 1 0 0-1.25a.625.625 0 0 0 0 1.25"/></svg>
              `;
                });
        });
    });
});