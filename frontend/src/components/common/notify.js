import { toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

// Success notification
export const successNotify = (msg) => {
    toast.success(msg, {
        position: "top-right", 
        autoClose: 3000,
    });

};

// Error notification
export const errorNotify = (msg) => {
    toast.error(msg, {
        position: "top-right", 
        autoClose: 3000,
    });
};

// Information notification
export const infoNotify = (msg) => {
    toast.info(msg, {
        position: "top-right", 
        autoClose: 3000,
    });
};

// Warning notification
export const warnNotify = (msg) => {
    toast.warn(msg, {
        position: "top-right", 
        autoClose: 3000,
    });
};
