window.InsightUI = window.InsightUI || {};

InsightUI.ThreeDCarousel = {
    init: function () {
        // Collect all elements with 'data-3D-carousel=<target_ID>'
        const threeDCarousels = []; // document.querySelectorAll("[data-3D-carousel]");

        threeDCarousels.forEach((carousel) => {
            // Media-Queries
            const screens = [
                window.matchMedia('(min-width: 640px)'),
                window.matchMedia('(min-width: 1024px)'),
                window.matchMedia('(min-width: 1536px)'),
                window.matchMedia('(min-width: 1920px)')
            ]

            // Distances: first -> smallest screen, last -> biggest screen
            const distances = [-1100, -750, -750, -550];
            const angle = 360 / 5;

            previous = document.getElementById("previous");
            next = document.getElementById("next");

            carousel = document.getElementById("threeD_carousel");

            let currentIndex = 0;

            function spin(index, toRight) {
                /* get the correct for the current window width (media-query) */
                distance = -850;
                for (let i = screens.length - 1; i >= 0; i--) {
                    if (screens[i].matches) {
                        distance = distances[i];
                        break;
                    }
                }

                /* adjust start index, in relation to the spin direction */
                fromIndex = index;

                if (toRight) fromIndex += 1;
                else fromIndex -= 1

                /* apply animation */
                return [
                    { transform: "translateX(-50%) perspective(1000px) translateZ(" + distance + "px) rotateX(-20deg) rotateY(" + (fromIndex * angle) + "deg)" },
                    { transform: "translateX(-50%) perspective(1000px) translateZ(" + distance + "px) rotateX(-20deg) rotateY(" + (index * angle) + "deg)" },
                ];
            }

            const spinSettings = {
                duration: 1000,
                fill: "forwards",
            };

            function gotoPrevious(event) {
                currentIndex++;
                if (currentIndex > 4) currentIndex = 0;

                carousel.animate(spin(currentIndex, false), spinSettings);
            }

            function gotoNext(event) {
                currentIndex--;
                if (currentIndex < 0) currentIndex = 4;

                carousel.animate(spin(currentIndex, true), spinSettings);
            }

            previous.addEventListener("click", gotoPrevious);
            next.addEventListener("click", gotoNext);
        });
    }
};
