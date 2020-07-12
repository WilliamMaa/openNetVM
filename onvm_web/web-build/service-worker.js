importScripts(
  "https://storage.googleapis.com/workbox-cdn/releases/3.6.2/workbox-sw.js"
);
importScripts("/precache-manifest.0cccbf17ef04e480d5436c2bffca8362.js");
workbox.clientsClaim();
self.__precacheManifest = [].concat(self.__precacheManifest || []);
workbox.precaching.suppressWarnings();
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
workbox.routing.registerNavigationRoute("/index.html", {
  blacklist: [/^\/_/, /\/[^/]+\.[^/]+$/]
});
