
/**
=====================================================================================
 C O P Y R I G H T
-------------------------------------------------------------------------------------
 Copyright (c) 2023 by Robert Bosch GmbH. All rights reserved.

 Author(s):
 - Aniket Salve, Robert Bosch Gmbh
=====================================================================================
*/


/**
 * This function stores and updates the session store with active href
 * If href is not present in nav bar then last state for session storage
 * is shown as active state in navbar
 *
 * The classes are customized for sphinx-rtd-theme
 */
function findCurrentRoute() {

    if (window.sessionStorage.getItem("href") == null) {
        window.sessionStorage.setItem("href", window.location.href);
    }

    if (document.querySelector("li.current")) {
        window.sessionStorage.setItem("href", window.location.href);
        return;
    } else {
        var lastActiveNav = window.sessionStorage.getItem("href");
        var allTags = document.querySelectorAll("li");
        for (let i = 0; i < allTags.length; i++) {
            if (allTags[i].getElementsByTagName("a")[0].href == lastActiveNav) {
                allTags[i].getElementsByTagName("a")[0].classList.add("current");
                allTags[i].getElementsByTagName("a")[0].setAttribute("aria-expanded", "true")
                allTags[i].classList.add("current");
                allTags[i].setAttribute("aria-expanded", "true")
                recursiveParentClassAppend(allTags[i].parentNode, true);
                return;
            }
        }
    }
}

/**
 * This function recursively parses the parent nodes
 * Adds current class to UL tags
 * Adds current class to LI tags
 * Adds aria-expanded attribute to UL and LI tags
 *
 * For all 2nd level and about parent UL nodes, the corresponding
 * input tag is checked so that the navbar is expanded. This is achieved using flag
 *
 * @param {ParentNode | null} element Parent node of last active LI tag
 * @param {Boolean} flag flag to check if input should be checked or not
 */
function recursiveParentClassAppend(element, flag) {
    if (element.nodeName == "UL") {
        element.classList.add("current")
        element.setAttribute("aria-expanded", "true")
        if (element.parentNode.nodeName == "LI") {
            element.parentNode.classList.add("current");
            element.parentNode.setAttribute("aria-expanded", "true")
            recursiveParentClassAppend(element.parentNode.parentNode, true);
        }
        else {
            return;
        }
    }
}

$(document).ready(function () {
    findCurrentRoute();
});
