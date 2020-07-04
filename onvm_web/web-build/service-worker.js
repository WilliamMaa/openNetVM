importScripts(
  "https://storage.googleapis.com/workbox-cdn/releases/3.6.2/workbox-sw.js"
);
importScripts("/precache-manifest.b59eddc05c9f421cabfa12f2783a6ddf.js");
workbox.clientsClaim();
self.__precacheManifest = [].concat(self.__precacheManifest || []);
workbox.precaching.suppressWarnings();
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
workbox.routing.registerNavigationRoute("/index.html", {
  blacklist: [/^\/_/, /\/[^/]+\.[^/]+$/]
});
