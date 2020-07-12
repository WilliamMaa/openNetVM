importScripts(
  "https://storage.googleapis.com/workbox-cdn/releases/3.6.2/workbox-sw.js"
);
importScripts("/precache-manifest.7a6177e43534b1e81e8b0e752fe34d1e.js");
workbox.clientsClaim();
self.__precacheManifest = [].concat(self.__precacheManifest || []);
workbox.precaching.suppressWarnings();
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
workbox.routing.registerNavigationRoute("/index.html", {
  blacklist: [/^\/_/, /\/[^/]+\.[^/]+$/]
});
