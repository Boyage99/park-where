const header = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
  const currentScroll = window.pageYOffset;
  if (currentScroll <= 10) {
    header.classList.remove('scroll');
  } else {
    header.classList.add('scroll');
  }
});

function removeCookie(cookieName) {
  document.cookie = cookieName + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

document.querySelector('.btn-logout').addEventListener('click', () => {
  alert('로그아웃합니다. 감사합니다');
  removeCookie('access_token');
  removeCookie('refresh_token');
  removeCookie('username');
  window.location.href = '/login';
});
