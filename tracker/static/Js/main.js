document.addEventListener("DOMContentLoaded", function () {

    const toasts = document.querySelectorAll(".toast");

    toasts.forEach(function(toast){

        const bsToast = new bootstrap.Toast(toast,{
            delay:3000
        });

        bsToast.show();

    });

});