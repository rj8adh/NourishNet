import React, {useState, useEffect} from "react";
import { BrowserMultiFormatReader } from "@zxing/library";


const BarcodeScanner = () => 
{
    const [result, setResult] = useState(null);
    const [videoDevice, setVideoDevice] = useState(null);

    useEffect(() => {
        const reader = new BrowserMultiFormatReader();
        async function init() {
            const videoDevices = await reader.listVideoInputDevices();
            if(videoDevices.length >0) {
                setVideoDevice(videoDevices[0]);
            }
        }

        init();
    },[]);

    useEffect(() =>{
        if(videoDevice) {
            const reader = new BrowserMultiFormatReader();
            reader.decodeFromVideoDevice(videoDevice.deviceId, "video",function (result) {
                    if (result) {
                        setResult(result.text);
                    }
                });
        }
    },[videoDevice]);

    return (
        <div>
            {result ? (
                <p>Scanned Code: {result}</p>
            ): (
                <p>Scanning</p>
            )}
        <video id="video" width = "600" height = "400"/>

        </div>
    );
};

export default BarcodeScanner;