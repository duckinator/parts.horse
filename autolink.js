// This is bad and I feel bad.
// Change <http://...> and <https://...> into proper links.
window.onload = function () {
  var text = document.body.innerHTML;
  document.body.innerHTML = text.replace(/<(https?:\/\/.*)>/, '<a href="$1">$1</a>')
}
