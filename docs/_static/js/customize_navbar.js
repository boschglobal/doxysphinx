

function findCurrentRute() {

    if (window.localStorage.getItem("href") == null) {
        window.localStorage.setItem("href", window.location.href);
    }

    if (document.querySelector("li.active")) {
        window.localStorage.setItem("href", window.location.href);
        return
    } else {
        var lastActiveNav = window.localStorage.getItem("href");
        var allTags = document.querySelectorAll("li")
        for (let i = 0; i < allTags.length; i++) {
            if (allTags[i].getElementsByTagName("a")[0].href == lastActiveNav) {
                allTags[i].classList.add("active")
                allTags[i].classList.add("current")
                recurriveParentClassAppend(allTags[i].parentElement);
            }
        }
        window.navigationDocument.pushDocument(document);
    }
}

function recurriveParentClassAppend(element) {
    if (element.nodeName == "UL") {
        element.classList.add("current")
        if (element.parentElement.nodeName == "LI") {
            element.parentElement.classList.add("active");
            element.parentElement.classList.add("current");
            recurriveParentClassAppend(element.parentElement.parentElement)
        }
        else {
            return
        }
    }
}

$(document).ready(function () {
    findCurrentRute()
});
