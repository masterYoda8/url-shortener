
var shortUrlAlreadyUsed = false;

create = async (short_url, original_url) => { 
    const url = "/";
    const payload = {
        "short_url": short_url,
        "original_url": original_url
    };
    const mapping = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
    })
        .then(response => response.ok ? response.json() : null)
        .catch(() => null);
    if (mapping !== null) {
        successAlert();
    } else {
        errorAlert();
    }
};

const handleShortUrlInput = async () => {
    const base_url = "/";
    const short_url = document.getElementById("shortUrlInput").value;
    if (short_url === "") {
        document.getElementById("shortUrlInput").classList.remove("is-valid");
        document.getElementById("shortUrlInput").classList.remove("is-invalid");
        return;
    }
    const queryParams = {
        noRedirect: true 
    };
    const params = new URLSearchParams(queryParams).toString();
    const url = `${base_url}${short_url}?${params}`;
    const mapping = await fetch(url, {
        method: "POST",
    })
        .then(response => response.ok ? response.json() : null)
        .catch(() => null);
    if (mapping !== null) {
        document.getElementById("invalidShort").innerHTML = `URL Mapping already in use! Still valid for ${getTimeDifferenceFromNow(mapping.created_at)}.`;
        document.getElementById("shortUrlInput").classList.add("is-invalid");
        document.getElementById("shortUrlInput").classList.remove("is-valid");
        shortUrlAlreadyUsed = true;
    } else {
        document.getElementById("shortUrlInput").classList.remove("is-invalid");
        document.getElementById("shortUrlInput").classList.add("is-valid");
        shortUrlAlreadyUsed = false;
    }
};

function setRandomShortUrl() {
    const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    const length = 4;
    const charactersLength = characters.length;
    let result = "";
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
    }
    document.getElementById("shortUrlInput").value = result;
}

function copyShortUrl() {
    let short_url = document.getElementById("shortUrlInput").value;
    let url = "https://url.remberger.dev/" + short_url;
    navigator.clipboard.writeText(url);
}

function successAlert() {
    let successAlert = document.getElementById("successAlert");
    successAlert.style.display = 'block';
    setTimeout(() => {
        successAlert.style.display = 'none';
    }, 3000);
}

function errorAlert() {
    let errorAlert = document.getElementById("errorAlert");
    errorAlert.style.display = 'block';
    setTimeout(() => {
        errorAlert.style.display = 'none';
    }, 3000);
}

function originalUrlInputHandler() {
    let original_url_input = document.getElementById("originalUrlInput");
    if (original_url_input.value.length) {
       original_url_input.classList.remove("is-invalid");
    } else {
       original_url_input.classList.add("is-invalid");
    }
}

const debouncedInputHandler = debounce(handleShortUrlInput, 500);

function debounce(func, wait) {
    let timeout;
    return function executeFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    }
}

document.getElementById("createButton").addEventListener('click', function(event) {
    let short_url = document.getElementById("shortUrlInput").value;
    let original_url = document.getElementById("originalUrlInput").value;
    handleShortUrlInput();
    if (!shortUrlAlreadyUsed && original_url.length && short_url.length) {
        create(short_url, original_url);
        shortUrlAlreadyUsed = true;
    }
    if (!original_url.length) {originalUrlInputHandler()}
    if (!short_url.length) {
        document.getElementById("invalidShort").innerHTML = "Empty string not allowed!";
        document.getElementById("shortUrlInput").classList.add("is-invalid");
    }
})

function getTimeDifferenceFromNow(datetimeString) {
    const datetime = new Date(datetimeString);
    datetime.setDate(datetime.getDate() + 90);
    const now = new Date();
    let difference = datetime - now;
    const seconds = Math.floor(difference / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    if (days > 1) {
        return `${days} days`;
    } else if (hours > 1) {
        return `${hours} hours`;
    } else if (minutes > 1) {
        return `${minutes} minutes`;
    } else {
        return `${seconds} seconds`;
    }
 }

document.getElementById("refreshButton").addEventListener('click', () => copyShortUrl());
document.getElementById("originalUrlInput").addEventListener('input', () => originalUrlInputHandler());
document.getElementById("shortUrlInput").addEventListener('input', debouncedInputHandler);
setRandomShortUrl();
handleShortUrlInput();