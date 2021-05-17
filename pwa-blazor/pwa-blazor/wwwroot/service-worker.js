// -Minimal service worker- 
// The goal of this service worker is to fulfill the requirement Chromium-browsers put on PWAs
// Hence, why it does nothing functional with the install and fetch events
self.addEventListener('install', function (event) { });
self.addEventListener('fetch', function (event) { });