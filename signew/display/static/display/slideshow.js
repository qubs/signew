/*
    Copyright 2016 the Queen's University Biological Station and
    the Signew Project Authors.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

"use strict";

/**
 * Creates the signew display slideshow object.
 * @constructor
 * @param {Object} A list of properties to initialize the slideshow object with.
 */
var SignewSlideshow = function (properties) {
    this.container = properties.container || "#signew-slides";
    this.slides = properties.slides || [];

    this.lastSlide = -1;
    this.currentSlide = 0;

    this.MEDIA_URL = properties.mediaURL || "/media/";

    this.URL_IMAGE = "URLI"
    this.URL_PAGE = "URLP"
    this.HOSTED_IMAGE = "HSTI"
    this.HOSTED_PAGE = "HSTP"

    this.$oldSlide = null;
    this.$newSlide = null;
};

/**
 * Adds a slide to the signew display slideshow.
 * @param {Object} Slide to add to the display's show.
 */
SignewSlideshow.prototype.addSlide = function (slide) {
    this.slides.push(slide);
};

/**
 * @param  {Object} The slide object to use to build the markup.
 * @return {Element} The slide element to add to the DOM.
 */
SignewSlideshow.prototype.makeSlide = function (slide) {
    var slideItem = document.createElement("li");
    slideItem.setAttribute("class", "signew-slide signew-slide-" + slide.type);
    slideItem.setAttribute("id", "signew-slide-" + slide.id);
    if (slide.type == this.URL_IMAGE) {
        slideItem.setAttribute("style", "background-image: url('" + slide.url + "')");
    } else if(slide.type == this.HOSTED_IMAGE) {
        slideItem.setAttribute("style", "background-image: url('" + this.MEDIA_URL + slide.file + "')");
    } else if (slide.type == this.URL_PAGE) {
        var slideFrame = document.createElement("iframe");
        slideFrame.setAttribute("class", "signew-slide-iframe");
        slideFrame.setAttribute("src", slide.url);
        slideItem.appendChild(slideFrame);
    } else if (slide.type == this.HOSTED_PAGE) {
        var slideFrame = document.createElement("iframe");
        slideFrame.setAttribute("class", "signew-slide-iframe");
        slideFrame.setAttribute("src", this.MEDIA_URL + slide.file);
        slideItem.appendChild(slideFrame);
    }

    if (slide.caption && slide.caption != "None") {
        var slideCaption = document.createElement("div");
        slideCaption.setAttribute("class", "signew-slide-caption");
        slideCaption.innerHTML = slide.caption;
        slideItem.appendChild(slideCaption);
    }

    return slideItem;
};

/**
 * Proceeds to the next slide in the signew display slideshow.
 */
SignewSlideshow.prototype.nextSlide = function () {
    this.lastSlide = this.currentSlide;
    this.currentSlide++;
    if(this.currentSlide == this.slides.length) {
        this.currentSlide = 0;
    }

    this.$oldSlide = $(this.container).children("#signew-slide-" + this.slides[this.lastSlide].id).first();
    this.$newSlide = $(this.container).children("#signew-slide-" + this.slides[this.currentSlide].id).first();

    this.$newSlide.css("transform", "translateX(100%)");
    this.$newSlide.addClass("active");

    this.$oldSlide.css("transform", "translateX(-100%)");
    window.setTimeout((function () {
        var d = new Date();

        if(this.slides[this.lastSlide].type == this.URL_IMAGE && this.slides[this.lastSlide].live) {
            this.$oldSlide.attr("style", "background-image: url('" + this.slides[this.lastSlide].url + "?"
                + d.getTime() + "')");
        }

        this.$oldSlide.removeClass("active");
    }).bind(this), 1000);

    this.$newSlide.animate({ "left": "0" }, 1000);
    this.$newSlide.css({ "transform": "translateX(0)" }, 1000);

    // Add a second to the timing for entry transition
    window.setTimeout(this.nextSlide.bind(this), this.slides[this.currentSlide].timing + 1000);
};

/**
 * Initializes the signew display slideshow.
 */
SignewSlideshow.prototype.initialize = function () {
    for(var s in this.slides) {
        if(this.slides.hasOwnProperty(s)) {
            $(this.container).append(this.makeSlide(this.slides[s]));
        }
    }

    $("#signew-slide-" + this.slides[this.currentSlide].id).addClass("active");

    if(slides.length != 1) {
        // Add a second to the timing for entry transition
        window.setTimeout(this.nextSlide.bind(this), this.slides[this.currentSlide].timing + 1000);
    }
};
