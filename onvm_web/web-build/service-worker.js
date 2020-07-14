importScripts(
  "https://storage.googleapis.com/workbox-cdn/releases/3.6.2/workbox-sw.js"
);
importScripts("/precache-manifest.56fb872459adcf21c8246c4c02b9907e.js");
workbox.clientsClaim();
self.__precacheManifest = [].concat(self.__precacheManifest || []);
workbox.precaching.suppressWarnings();
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
workbox.routing.registerNavigationRoute("/index.html", {
  blacklist: [/^\/_/, /\/[^/]+\.[^/]+$/]
});
