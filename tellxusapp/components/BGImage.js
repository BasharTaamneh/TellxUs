import { useEffect, useState } from "react";

function getWindowDimensions() {
    const { innerWidth: width, innerHeight: height } = window;
    return {
        width,
        height,
    };
}

function BGImage() {
    const [width, setWidth] = useState();
    const [height, setheight] = useState();

    useEffect(() => {
        const { width, height } = getWindowDimensions();

        setWidth(width);

        setheight(height);
    }, []);

    useEffect(() => {
        function handleResize() {
            const { width, height } = getWindowDimensions();

            setWidth(width);

            setheight(height);
        }

        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    if (width && height) {
        return (
            { width, height }
        )
    }

    return null;
}

export default BGImage;