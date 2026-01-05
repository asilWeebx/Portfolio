import logo from '../../assets/dev.png';
import meImage from '../../assets/me.jpg';

function LeftSidebarMobile() {
    return (
        <div className="left-sidebar">
            <div className="sidebar-header d-flex align-items-center justify-content-between">
                <img src={logo} alt="Logo" width="150px" />
                <span className="designation"></span>
            </div>

            <h2 className="email">hi@asilbek-yuldashev.uz</h2>
            <h2 className="address">Uzbekistan, Karshi</h2>
            <p className="copyright">
                &copy; 2023 - {new Date().getFullYear()} Devnity. All rights reserved.
            </p>
            <ul className="social-profile d-flex align-items-center flex-wrap justify-content-center">
                <li>
                    <a href="https://t.me/iamyshv" target="_blank" rel="noreferrer">
                        <i className="lab la-telegram"></i>
                    </a>
                </li>
                <li>
                    <a href="https://instagram.com/devnity.uz" target="_blank" rel="noreferrer">
                        <i className="lab la-instagram"></i>
                    </a>
                </li>
                <li>
                    <a href="https://github.com/asilweebx" target="_blank" rel="noreferrer">
                        <i className="lab la-github"></i>
                    </a>
                </li>
            </ul>
            <a href="tel:+998978022008" target="_blank" className="theme-btn" rel="noreferrer">
                <i className="las la-envelope"></i> Contact
            </a>
        </div>
    );
}

export default LeftSidebarMobile;
