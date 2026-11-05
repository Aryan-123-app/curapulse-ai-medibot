"use client";

// use client

import { useEffect, useRef, useState } from "react";
import type { FormEvent, KeyboardEvent, ReactNode } from "react";
import Image from "next/image";
import ReactMarkdown from "react-markdown";

type Source = {
  source: string;
  page: number | string;
  excerpt: string;
};

type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

type IconName = "spark" | "book" | "chat" | "plus" | "arrow" | "refresh" | "close" | "send" | "reference" | "menu";

function Icon({ name }: { name: IconName }) {
  const paths: Record<IconName, ReactNode> = {
    spark: <path d="m12 3 2.1 6.2L20 12l-5.9 2.1L12 20l-2.1-5.9L4 12l5.9-2.8L12 3Z" />,
    book: <><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v16H6.5A2.5 2.5 0 0 0 4 21V5.5Z" /><path d="M4 17a2.5 2.5 0 0 1 2.5-2.5H20M8 7h7" /></>,
    chat: <><path d="M20 11.5a7.5 7.5 0 0 1-7.5 7.5H5l1.8-3.1A7.5 7.5 0 1 1 20 11.5Z" /><path d="M9 11h.01M12.5 11h.01M16 11h.01" /></>,
    plus: <><path d="M12 5v14M5 12h14" /></>,
    arrow: <><path d="M7 17 17 7M7 7h10v10" /></>,
    refresh: <><path d="M20 7v5h-5M4 17v-5h5" /><path d="M5.6 9A7 7 0 0 1 17 6l3 6M4 12l3 6a7 7 0 0 0 11.4-3" /></>,
    close: <><path d="m6 6 12 12M18 6 6 18" /></>,
    send: <><path d="m21 3-7.2 18-3.7-7.1L3 10.2 21 3Z" /><path d="M10.1 13.9 15 9" /></>,
    reference: <><path d="M10.5 18a7.5 7.5 0 1 1 5.3-2.2" /><path d="m16 16 4.5 4.5M8 10h5M8 13h3" /></>,
    menu: <><path d="M4 7h16M4 12h16M4 17h16" /></>,
  };

  return (
    <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      {paths[name]}
    </svg>
  );
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const SUGGESTIONS = [
  "What are the symptoms of asthma?",
  "How is diabetes diagnosed?",
  "What is cancer?",
];
const ABOUT_SLIDES = [
  {
    src: "/health-professional.jpg",
    alt: "A healthcare professional in a white coat",
    label: "HEALTH KNOWLEDGE, MADE APPROACHABLE",
    title: <>Clarity begins<br />with a good question.</>,
    position: "50% 35%",
  },
  {
    src: "/about-consultation.jpg",
    alt: "A surgical team collaborating in an operating room",
    label: "BETTER CARE STARTS WITH COLLABORATION",
    title: <>Knowledge grows<br />through collaboration.</>,
    position: "50% 50%",
  },
  {
    src: "/about-research-alt.jpg",
    alt: "A medical researcher working with laboratory equipment",
    label: "KNOWLEDGE ROOTED IN RESEARCH",
    title: <>Explore the science.<br />Keep learning.</>,
    position: "50% 50%",
  },
];

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [question, setQuestion] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [chatOpen, setChatOpen] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [expandedSource, setExpandedSource] = useState<number | null>(null);
  const [openFAQ, setOpenFAQ] = useState<number | null>(0);
  const [aboutSlide, setAboutSlide] = useState(0);
  const endOfMessages = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    endOfMessages.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  useEffect(() => {
    if (chatOpen) inputRef.current?.focus();
  }, [chatOpen]);

  async function sendQuestion(text = question) {
    const trimmedQuestion = text.trim();
    if (!trimmedQuestion || isLoading) return;

    const history = messages.slice(-40);
    setMessages((current) => [...current, { role: "user", content: trimmedQuestion }]);
    setQuestion("");
    setError("");
    setIsLoading(true);
    setChatOpen(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmedQuestion, history }),
      });
      const result: { answer?: string; sources?: Source[]; detail?: string } =
        await response.json();

      if (!response.ok) {
        throw new Error(result.detail ?? "The assistant could not answer right now.");
      }

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: result.answer ?? "No response was returned.",
          sources: result.sources ?? [],
        },
      ]);
    } catch (requestError) {
      setError(
        requestError instanceof Error
          ? requestError.message
          : "Could not connect to the CuraPulse API.",
      );
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void sendQuestion();
  }

  function handleInputKeyDown(event: KeyboardEvent<HTMLInputElement>) {
    if (event.key === "Escape") setChatOpen(false);
  }

  function clearConversation() {
    setMessages([]);
    setError("");
    setExpandedSource(null);
  }

  return (
    <main>
      <header className={`topbar${mobileMenuOpen ? " menu-open" : ""}`}>
        <a className="wordmark" href="#home" aria-label="CuraPulse home">
          CURAPULSE<span>.</span>
        </a>
        <button
          className="mobile-menu-toggle"
          type="button"
          aria-label={mobileMenuOpen ? "Close navigation menu" : "Open navigation menu"}
          aria-expanded={mobileMenuOpen}
          aria-controls="primary-navigation"
          onClick={() => setMobileMenuOpen((open) => !open)}
        >
          <Icon name={mobileMenuOpen ? "close" : "menu"} />
        </button>
        <button className="button button-dark topbar-cta" onClick={() => setChatOpen(true)}>
          Talk to CuraPulse <span className="button-icon"><Icon name="arrow" /></span>
        </button>
        <nav className="main-nav" id="primary-navigation" aria-label="Main navigation">
          <a className="active" href="#home" onClick={() => setMobileMenuOpen(false)}>Home</a>
          <a href="#about" onClick={() => setMobileMenuOpen(false)}>About</a>
          <a href="#technology" onClick={() => setMobileMenuOpen(false)}>Technology</a>
          <a href="#services" onClick={() => setMobileMenuOpen(false)}>Services</a>
        </nav>
      </header>

      <section className="hero" id="home">
        <Image
          className="hero-visual"
          src="/hero-robot.png"
          alt=""
          aria-hidden="true"
          width={500}
          height={500}
          priority
        />
        <div className="hero-copy">
          <span className="eyebrow"><span className="status-dot" /> Evidence-led medical AI</span>
          <h1>Revolutionizing Healthcare with AI</h1>
          <p className="hero-description">
            Get clear, thoughtful answers grounded in trusted medical literature.
            Explore health topics with an AI assistant designed to put reliable
            clinical knowledge within reach.
          </p>
          <div className="hero-actions">
            <button className="button button-dark" onClick={() => setChatOpen(true)}>
              Ask a clinical question <span className="button-icon"><Icon name="arrow" /></span>
            </button>
            <a className="button button-outline" href="#about">Discover CuraPulse</a>
          </div>
          <div className="proof-row">
            <div className="avatar-stack" aria-hidden="true">
              <span>MED</span><span>REF</span><span>AI</span>
            </div>
            <p><strong>3,282+ clinical references</strong><br />Answers supported by a trusted medical encyclopedia</p>
          </div>
        </div>

      </section>

      <section className="trust-strip" aria-label="CuraPulse highlights">
        <a className="trust-item" href="#technology">
          <span className="trust-item-icon" aria-hidden="true"><Icon name="book" /></span>
          <span className="trust-item-copy"><strong>Reference-led</strong><small>Explore a medical knowledge library</small></span>
          <span className="trust-item-arrow" aria-hidden="true"><Icon name="arrow" /></span>
        </a>
        <a className="trust-item" href="#technology">
          <span className="trust-item-icon" aria-hidden="true"><Icon name="reference" /></span>
          <span className="trust-item-copy"><strong>Sources in view</strong><small>See citations alongside answers</small></span>
          <span className="trust-item-arrow" aria-hidden="true"><Icon name="arrow" /></span>
        </a>
        <button className="trust-item" onClick={() => setChatOpen(true)}>
          <span className="trust-item-icon" aria-hidden="true"><Icon name="chat" /></span>
          <span className="trust-item-copy"><strong>Ask naturally</strong><small>Continue with a follow-up</small></span>
          <span className="trust-item-arrow" aria-hidden="true"><Icon name="arrow" /></span>
        </button>
        <a className="trust-item" href="#services">
          <span className="trust-item-icon" aria-hidden="true"><Icon name="plus" /></span>
          <span className="trust-item-copy"><strong>Made for learning</strong><small>Educational support, clearly stated</small></span>
          <span className="trust-item-arrow" aria-hidden="true"><Icon name="arrow" /></span>
        </a>
      </section>

      <section className="about-section section-band" id="about">
        <div className="content-section section-shell">
        <div className="section-intro">
          <div>
            <span className="section-label">ABOUT CURAPULSE</span>
            <h2>Medical knowledge,<br /><em>made easier to explore.</em></h2>
          </div>
          <p>
            Health information can be difficult to navigate. CuraPulse brings
            conversational AI together with a searchable medical reference library
            to make educational topics easier to explore.
          </p>
        </div>

        <div className="about-editorial">
          <figure className="about-photo">
            <Image
              key={ABOUT_SLIDES[aboutSlide].src}
              className="about-photo-image"
              src={ABOUT_SLIDES[aboutSlide].src}
              alt={ABOUT_SLIDES[aboutSlide].alt}
              fill
              sizes="(max-width: 800px) 100vw, 48vw"
              unoptimized
              style={{ objectPosition: ABOUT_SLIDES[aboutSlide].position }}
            />
            <span className="about-photo-mark" aria-hidden="true"><Icon name="spark" /></span>
            <figcaption>
              <span>{ABOUT_SLIDES[aboutSlide].label}</span>
              <strong>{ABOUT_SLIDES[aboutSlide].title}</strong>
            </figcaption>
            <nav className="about-photo-pagination" aria-label="About image slides">
              {ABOUT_SLIDES.map((slide, index) => (
                <button
                  key={slide.src}
                  type="button"
                  className={aboutSlide === index ? "is-active" : ""}
                  aria-label={`Show image ${index + 1} of ${ABOUT_SLIDES.length}: ${slide.label.toLowerCase()}`}
                  aria-pressed={aboutSlide === index}
                  onClick={() => setAboutSlide(index)}
                >
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <i>/ 03</i>
                </button>
              ))}
            </nav>
          </figure>
          <div className="about-story">
            <span className="feature-number">A MORE THOUGHTFUL EXPERIENCE</span>
            <h3>Ask naturally.<br /><em>Understand the context.</em></h3>
            <p>
              Health information can feel overwhelming. CuraPulse gives you a
              calmer place to begin: ask in everyday language and explore an
              educational explanation grounded in indexed medical references.
            </p>
            <p>
              When sources are available, review their details alongside the
              response. When you need more context, keep the conversation going.
            </p>
            <button className="text-link" onClick={() => setChatOpen(true)}>
              Meet your research companion <span className="button-icon"><Icon name="arrow" /></span>
            </button>
            <blockquote>
              <span aria-hidden="true">“</span>
              <p>Built to support curiosity—not to replace professional care.</p>
            </blockquote>
          </div>
        </div>
        <div className="about-principles">
          <article><span>01</span><div><h3>Understand</h3><p>Clear, conversational explanations for general health topics.</p></div></article>
          <article><span>02</span><div><h3>Explore</h3><p>Reference details that help you continue learning.</p></div></article>
          <article><span>03</span><div><h3>Stay informed</h3><p>Educational support with the limits made clear.</p></div></article>
        </div>
        </div>
      </section>

      <section className="feature-section section-band" id="technology">
        <div className="content-section section-shell">
        <div className="section-intro technology-heading">
          <div>
            <span className="section-label">HOW THE ASSISTANT WORKS</span>
            <h2>From question<br /><em>to useful context.</em></h2>
          </div>
          <p>
            A simple flow brings together your question, relevant reference content,
            and a conversational response you can explore.
          </p>
        </div>
        <div className="process-layout">
          <div className="process-list">
            <article>
              <span className="process-number">01</span>
              <div><h3>Ask in your own words</h3><p>Start with a general health question or choose a suggested prompt.</p></div>
            </article>
            <article>
              <span className="process-number">02</span>
              <div><h3>Find relevant context</h3><p>The assistant retrieves related content from its indexed reference library.</p></div>
            </article>
            <article>
              <span className="process-number">03</span>
              <div><h3>Explore the response</h3><p>Read an educational explanation, inspect available citations, and ask a follow-up.</p></div>
            </article>
          </div>
          <figure className="process-photo">
            <Image
              src="/doctor-phone.jpg"
              alt="A doctor reviewing health information on a phone"
              fill
              sizes="(max-width: 800px) 100vw, 55vw"
              unoptimized
            />
            <figcaption>
              <span>YOUR QUESTION, WITH CONTEXT</span>
              <strong>Information you can explore.</strong>
            </figcaption>
            <div className="process-source-note">
              <span className="process-source-label"><span className="process-source-icon"><Icon name="reference" /></span>REFERENCE FOUND</span>
              <strong>Relevant medical context</strong>
              <small>Source details available with the response</small>
            </div>
          </figure>
        </div>
        <div className="response-note">
          <span className="response-note-mark"><Icon name="spark" /></span>
          <div><strong>Explanation and sources, together.</strong><p>Review available citations and excerpts alongside the assistant’s response.</p></div>
          <span className="response-note-link" aria-hidden="true"><Icon name="arrow" /></span>
        </div>
        <p className="technology-note">
          CuraPulse is an educational tool. Its responses may be incomplete or
          inaccurate and should not be used to diagnose or treat a condition.
        </p>
        </div>
      </section>

      <section className="faq-section section-band" id="services">
        <div className="content-section section-shell">
        <div className="section-intro faq-heading">
          <div>
            <span className="section-label">A FEW THINGS TO KNOW</span>
            <h2>Questions worth<br /><em>asking first.</em></h2>
          </div>
          <p>Learn what CuraPulse can help with, how to explore references, and when to seek professional care.</p>
        </div>
        <div className="faq-layout">
          <div className="faq-list" aria-label="Frequently asked questions">
            {[
              {
                question: "What is CuraPulse?",
                answer: "CuraPulse is an educational AI assistant that helps you explore general health topics using a searchable medical reference library. It is not a medical provider.",
              },
              {
                question: "Where do the answers come from?",
                answer: "Responses are generated using relevant content retrieved from CuraPulse’s indexed medical reference material. Available citations and excerpts can be reviewed alongside an answer.",
              },
              {
                question: "Can CuraPulse diagnose or treat me?",
                answer: "No. CuraPulse is for educational purposes only and cannot diagnose, treat, or replace advice from a qualified healthcare professional. Seek professional guidance for personal medical concerns.",
              },
              {
                question: "Can I ask follow-up questions?",
                answer: "Yes. Continue the conversation to ask for clarification or explore a topic further. Always verify important health decisions with a qualified healthcare professional.",
              },
            ].map((item, index) => {
              const isOpen = openFAQ === index;
              const triggerId = `faq-trigger-${index + 1}`;
              const panelId = `faq-panel-${index + 1}`;

              return (
                <article className={`faq-item${isOpen ? " is-open" : ""}`} key={item.question}>
                  <h3 className="faq-question-heading">
                    <button
                      className="faq-question-button"
                      id={triggerId}
                      type="button"
                      aria-expanded={isOpen}
                      aria-controls={panelId}
                      onClick={() => setOpenFAQ(isOpen ? null : index)}
                    >
                      <span className="faq-number">{String(index + 1).padStart(2, "0")}</span>
                      <span className="faq-question">{item.question}</span>
                      <span className="faq-icon" aria-hidden="true"><Icon name="plus" /></span>
                    </button>
                  </h3>
                  <div
                    className="faq-panel"
                    id={panelId}
                    role="region"
                    aria-labelledby={triggerId}
                    aria-hidden={!isOpen}
                  >
                    <div className="faq-panel-inner">
                      <p>{item.answer}</p>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
          <aside className="faq-aside">
            <div className="faq-aside-art">
              <Image src="/dna-helix.jpg" alt="" aria-hidden="true" width={1024} height={1024} />
              <span className="faq-art-orbit faq-art-orbit-one" />
              <span className="faq-art-orbit faq-art-orbit-two" />
            </div>
            <span className="feature-number">CURIOUS? START HERE.</span>
            <h3>Ask a question.<br /><em>Explore at your pace.</em></h3>
            <p>Get an educational overview and review the references available with your response.</p>
            <button className="button button-dark" onClick={() => setChatOpen(true)}>
              Ask CuraPulse <span className="button-icon"><Icon name="arrow" /></span>
            </button>
          </aside>
        </div>
        </div>
      </section>

      <footer className="footer">
        <div className="footer-main">
          <div className="footer-brand">
            <a className="wordmark" href="#home">CURAPULSE<span>.</span></a>
            <p>Grounded knowledge. A more thoughtful way to explore health information.</p>
          </div>
          <div className="footer-links">
            <div>
              <h3>Explore</h3>
              <a href="#home">Home</a>
              <a href="#about">About CuraPulse</a>
              <a href="#technology">How it works</a>
              <a href="#services">Explore topics</a>
            </div>
            <div>
              <h3>Get started</h3>
              <button onClick={() => setChatOpen(true)}>Ask a question <span className="button-icon"><Icon name="arrow" /></span></button>
              <a href="#technology">References &amp; citations</a>
              <a href="#services">Educational use</a>
            </div>
          </div>
        </div>
        <div className="footer-bottom">
          <span>© {new Date().getFullYear()} CuraPulse. For educational purposes only.</span>
          <p>Not medical advice. CuraPulse does not diagnose, treat, or replace a qualified healthcare professional. For personal medical concerns, consult a healthcare professional.</p>
        </div>
      </footer>

      {chatOpen && (
        <div className="chat-backdrop" onMouseDown={(event) => {
          if (event.target === event.currentTarget) setChatOpen(false);
        }}>
          <section className="chat-panel" role="dialog" aria-modal="true" aria-labelledby="chat-title">
            <header className="chat-header">
              <div className="chat-brand">
                <span className="chat-mark"><Icon name="spark" /></span>
                <span><strong id="chat-title">CuraPulse assistant</strong><small><span className="status-dot" /> Grounded in medical literature</small></span>
              </div>
              <div className="chat-controls">
                <button className="icon-button" onClick={clearConversation} aria-label="Clear conversation" title="Clear conversation"><Icon name="refresh" /></button>
                <button className="icon-button close-button" onClick={() => setChatOpen(false)} aria-label="Close assistant"><Icon name="close" /></button>
              </div>
            </header>

            <div className="chat-messages">
              {messages.length === 0 && (
                <div className="chat-welcome">
                  <span className="welcome-icon"><Icon name="spark" /></span>
                  <h2>What would you like to understand?</h2>
                  <p>Ask about symptoms, conditions, or diagnostic tests. Responses are educational and cite their sources.</p>
                  <div className="suggestion-list">
                    {SUGGESTIONS.map((suggestion) => (
                      <button key={suggestion} onClick={() => void sendQuestion(suggestion)}>
                        {suggestion}<span className="button-icon"><Icon name="arrow" /></span>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {messages.map((message, index) => (
                <article className={`message message-${message.role}`} key={`${index}-${message.content.slice(0, 20)}`}>
                  <span className={`message-avatar message-avatar-${message.role}`} aria-hidden="true">
                    {message.role === "assistant" ? <Icon name="spark" /> : "YOU"}
                  </span>
                  <div className="message-body">
                    <span className="message-author">{message.role === "assistant" ? "CURAPULSE" : "YOU"}</span>
                    <div className="markdown-content">
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                    </div>
                    {message.sources && message.sources.length > 0 && (
                      <div className="sources">
                        <button className="sources-toggle" onClick={() => setExpandedSource(expandedSource === index ? null : index)}>
                          <span className="sources-mark"><Icon name="reference" /></span> View {message.sources.length} cited {message.sources.length === 1 ? "source" : "sources"}
                          <span className={`sources-chevron${expandedSource === index ? " is-open" : ""}`}><Icon name="plus" /></span>
                        </button>
                        {expandedSource === index && message.sources.map((source, sourceIndex) => (
                          <div className="source-card" key={`${source.source}-${source.page}-${sourceIndex}`}>
                            <span className="source-index">SOURCE 0{sourceIndex + 1}</span>
                            <strong>{source.source}</strong>
                            <span className="source-page">Page {source.page}</span>
                            <p>{source.excerpt}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </article>
              ))}

              {isLoading && <div className="thinking"><span /><span /><span /> Searching trusted sources…</div>}
              {error && <div className="chat-error" role="alert">{error}</div>}
              <div ref={endOfMessages} />
            </div>

            <form className="chat-composer" onSubmit={handleSubmit}>
              <input
                ref={inputRef}
                value={question}
                onChange={(event) => setQuestion(event.target.value)}
                onKeyDown={handleInputKeyDown}
                placeholder="Ask a clinical or medical question…"
                aria-label="Your question"
                maxLength={4000}
                disabled={isLoading}
              />
              <button type="submit" className="send-button" disabled={!question.trim() || isLoading} aria-label="Send question">
                <Icon name="send" />
              </button>
            </form>
            <p className="chat-disclaimer">Educational information only. For medical concerns, consult a qualified healthcare professional.</p>
          </section>
        </div>
      )}
    </main>
  );
}
