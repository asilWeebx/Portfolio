import { useLayoutEffect } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

import Home from "./components/home";
import About from "./components/about";
import Resume from "./components/resume";
import Services from "./components/services";
import Skills from "./components/skills";
import Portfolio from "./components/portfolio";
import Pricing from "./components/pricing";
import Contact from "./components/contact";
import SidebarMenu from "./components/sidebar-menu";
import ScrollNav from "./components/scroll-nav";
import LeftSidebar from "./components/left-sidebar";
import LeftSidebarMobile from "./components/left-sidebar-mobile";
import BodyOverlay from "./components/body-overlay";

gsap.registerPlugin(ScrollTrigger);

function App() {
  useLayoutEffect(() => {
    const ctx = gsap.context(() => {
      const defaults = {
        duration: 1.2,
        ease: "power4.out",
        animation: "fade_from_bottom",
      };

      const animations = {
        fade_from_bottom: { y: 120, opacity: 0 },
        fade_from_top: { y: -120, opacity: 0 },
        fade_from_left: { x: -120, opacity: 0 },
        fade_from_right: { x: 120, opacity: 0 },
        fade_in: { opacity: 0 },
        rotate_up: { y: 120, rotation: 10, opacity: 0 },
      };

      gsap.utils.toArray(".scroll-animation").forEach((el) => {
        const anim =
          animations[el.dataset.animation] ||
          animations[defaults.animation];

        gsap.from(el, {
          ...anim,
          duration:
            parseFloat(el.dataset.animationDuration) || defaults.duration,
          ease: defaults.ease,
          scrollTrigger: {
            trigger: el,
            start: "top 85%",
            toggleActions: "play none none reverse",
          },
        });
      });

      ScrollTrigger.refresh();
    });

    return () => ctx.revert();
  }, []);

  return (
    <div className="home-page">
      <BodyOverlay />
      <SidebarMenu />
      <ScrollNav />
      <LeftSidebar />

      <main className="drake-main">
        <LeftSidebarMobile />

        <Home />
        <About />
        <Resume />
        <Services />
        <Skills />
        <Portfolio />
        <Pricing />
        <Contact />
      </main>
    </div>
  );
}

export default App;
