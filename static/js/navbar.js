const header = document.querySelector('.navbar');
window.addEventListener("scroll", () => {
    const currentScroll = window.pageYOffset;
    if (currentScroll <= 10) {
        header.classList.remove('scroll');
    } else {
        header.classList.add('scroll');
    }
});