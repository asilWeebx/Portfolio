import { ArrowLeft } from 'lucide-react'
import { Link } from 'react-router-dom'
import Seo from '../components/Seo'

export default function NotFound() {
  return (
    <section className="not-found">
      <Seo title="Sahifa topilmadi" />
      <div className="hero__bg" aria-hidden="true" />
      <div className="hero__shade" aria-hidden="true" />
      <div className="container not-found__inner">
        <span className="not-found__code">404</span>
        <h1>Bu cho'qqi hali zabt etilmagan</h1>
        <p>Siz qidirgan sahifa topilmadi yoki ko'chirilgan.</p>
        <Link to="/" className="btn btn--primary btn--lg"><ArrowLeft size={20} /> Bosh sahifaga</Link>
      </div>
    </section>
  )
}
