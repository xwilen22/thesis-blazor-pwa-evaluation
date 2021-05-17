const SERVICE_WORKER_URL = `${process.env.PUBLIC_URL}/service-worker-min.js`

export function registerMinServiceWorker() {
    if('serviceWorker' in navigator) {
        navigator.serviceWorker
        .register(SERVICE_WORKER_URL)
        .then((registration) => {
          console.log("Registered minimal service worker: ", registration)
        })
        .catch((error) => {
          console.error("Error during service worker registration:", error);
        });
    }
    else {
        console.error("Browser does not support service workers")
    }
}