function Resume() {
    const experienceData = [
       {
        date: '2023 - 2024',
        title: 'Backend Developer',
        place: 'IT City Academy',
    },
    ];

    const educationData = [
        {
        date: '2025 - Present',
        title: "Bachelor’s Degree in Information Technology",
        place: 'INHA University in Tashkent (IUT), Faculty of IT',
    },
    {
        date: '2023-2024',
        title: 'Front-end & Back-end Development',
        place: 'Mohirdev',
    },
    {
        date: '2022',
        title: 'Full Stack Python Development',
        place: 'IT City Academy',
    },
        {
            date: '2023 - 2024',
            title: 'WordPress & Django REST Framework',
            place: 'YouTube',
        },
    ];

    return (
        <section className="resume-area page-section scroll-to-page" id="resume">
            <div className="custom-container">
                <div className="resume-content content-width">
                    <div className="section-header scroll-animation" data-animation="fade_from_bottom">
                        <h4 className="subtitle">
                            <i className="las la-briefcase"></i> Resume
                        </h4>
                        <h1>
                            Education and&nbsp;<span>Experience</span>
                        </h1>
                    </div>

                    <div className="resume-timeline">
                         {/* --- Education Section --- */}
                        {educationData.map((item, index) => (
                            <div
                                key={index + 100}
                                className="item scroll-animation"
                                data-animation="fade_from_right"
                            >
                                <span className="date">{item.date}</span>
                                <h2>{item.title}</h2>
                                <p>{item.place}</p>
                            </div>
                        ))}
                        {/* --- Experience Section --- */}
                        {experienceData.map((item, index) => (
                            <div
                                key={index}
                                className="item scroll-animation"
                                data-animation="fade_from_right"
                            >
                                <span className="date">{item.date}</span>
                                <h2>{item.title}</h2>
                                <p>{item.place}</p>
                            </div>
                        ))}

                       
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Resume;
