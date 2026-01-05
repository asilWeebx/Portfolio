function About() {
    return (
        <section className="about-area page-section scroll-to-page" id="about">
            <div className="custom-container">
                <div className="about-content content-width">
                    <div className="section-header">
                        <h4 className="subtitle scroll-animation" data-animation="fade_from_bottom">
                            <i className="lar la-user"></i> About Me
                        </h4>
                        <h1 className="scroll-animation" data-animation="fade_from_bottom">
                            My name is&nbsp;
                            <span>Asilbek Yuldashev</span>
                        </h1>
                    </div>
                    <p className="scroll-animation" data-animation="fade_from_bottom">
                        I am a backend developer and a student at INHA University. I have experience in building web applications and enjoy solving complex problems to create efficient, user-friendly solutions. I am always eager to learn new technologies and improve my skills. In my free time, I like exploring new tech trends and working on personal projects.is both eye-catching and easy to use. 
                        My goal is to convey your message and identity creatively.
                    </p>
                    <div className="row mt-3 scroll-animation row-cols-1 row-cols-md-2" data-animation="fade_from_bottom">
                        <div className="col scroll-animation" data-animation="fade_from_left">
                            <ul>
                                <li>Name: Asilbek</li>
                                <li>Surname: Yuldashev</li>
                                <li>Age: {new Date().getFullYear() - 2007}</li>
                                <li>  Level: {(() => {
    const experience = new Date().getFullYear() - 2022; // Ish boshlagan yilni kiriting
    if (experience < 2) return "Junior Developer";
    if (experience < 5) return "Middle Developer";
    return "Senior Developer";
  })()}</li>
                            </ul>
                        </div>
                        <div className="col scroll-animation" data-animation="fade_from_right">
                            <ul>
                                <li>Phone: +998 97 802 2008</li>
                                <li>Email: hi@asilbek-yuldashev.uz</li>
                                <li>ZIP Code: 180100</li>
                                <li>Address: Uzbekistan, Karshi</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default About;
