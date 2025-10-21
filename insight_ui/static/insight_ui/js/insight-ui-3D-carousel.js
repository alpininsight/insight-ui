window.InsightUI = window.InsightUI || {};

InsightUI.ThreeDCarousel = {
    init: function () {
        // Collect all elements with 'data-3D-carousel=<target_ID>'
        const threeDCarousels = document.querySelectorAll("[data-3D-carousel]");

        threeDCarousels.forEach((carouselWrapper) => {
            // Media-Queries
            const screens = [
                window.matchMedia('(min-width: 640px)'),
                window.matchMedia('(min-width: 1024px)'),
                window.matchMedia('(min-width: 1536px)'),
                window.matchMedia('(min-width: 1920px)')
            ]

            const face_camera = carouselWrapper.getAttribute("data-carousel-face-camera") === 'true';
            const carousel = carouselWrapper.firstElementChild;
            const previous = carouselWrapper.lastElementChild.firstElementChild;
            const next = carouselWrapper.lastElementChild.lastElementChild;

            // Distances: first -> smallest screen, last -> biggest screen
            const distances = [-1100, -750, -750, -550];
            const itemsCount = carousel.children.length;
            const angle = 360 / itemsCount;
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
                    { transform: "translateX(-50%) perspective(1000px) translateZ(" + distance + "px) rotateX(var(--carousel-tilt)) rotateY(" + (fromIndex * angle) + "deg)" },
                    { transform: "translateX(-50%) perspective(1000px) translateZ(" + distance + "px) rotateX(var(--carousel-tilt)) rotateY(" + (index * angle) + "deg)" },
                ];
            }

            const spinSettings = {
                duration: parseInt(carouselWrapper.getAttribute("data-carousel-velocity")),
                fill: "forwards",
            };

            function gotoPrevious(event) {
                currentIndex++;
                carousel.animate(spin(currentIndex, false), spinSettings);

                if (face_camera)
                {
                    for (let item of carousel.children)
                    {
                        item.firstElementChild.animate([{ transform: "rotateY(calc((var(--position) + " + currentIndex + " - 1) * (360 / var(--quantity)) * -1deg)) rotateX(calc(var(--carousel-tilt) * -1))" }], spinSettings);
                    }
                }
            }

            function gotoNext(event) {
                currentIndex--;
                carousel.animate(spin(currentIndex, true), spinSettings);

                if (face_camera)
                {
                    for (let item of carousel.children)
                    {
                        item.firstElementChild.animate([{ transform: "rotateY(calc((var(--position) + " + currentIndex + " - 1) * (360 / var(--quantity)) * -1deg)) rotateX(calc(var(--carousel-tilt) * -1))" }], spinSettings);
                    }
                }
            }

            previous.addEventListener("click", gotoPrevious);
            next.addEventListener("click", gotoNext);
        });
    }
};
