import { Link } from "react-router-dom";
import React from "react";

const NavBar = () => {
    return (
            <div className="navbar">
                <div><img className={"logo_slika"} src={"vms.jpg"} alt={"logo_slika"}/></div>
                <div className="logo">КРИПТО АНАЛИЗА</div>
                <div className="nav-links">
                    <Link to="/">Почетна</Link>
                    <Link to="/about">За нас</Link>
                    <Link to="/contact">Контакт</Link>
                </div>
            </div>
    );
};

export default NavBar;
