<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JW Multiple Player Pro</title>
    <!-- React 및 필수 라이브러리 CDN -->
    <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    
    <style>
        /* 커스텀 스크롤바 */
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { border-radius: 10px; }
        .dark .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); }
        .light .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #1E6F54; }
        
        mark { color: inherit; border-radius: 2px; }

        /* 슬라이더 스타일 커스텀 */
        input[type=range] { -webkit-appearance: none; background: transparent; }
        input[type=range]:focus { outline: none; }
        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            height: 16px;
            width: 16px;
            border-radius: 50%;
            background: #1E6F54; 
            cursor: pointer;
            margin-top: -6px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.3);
        }
        input[type=range]::-webkit-slider-runnable-track {
            width: 100%;
            height: 4px;
            cursor: pointer;
            background: rgba(30, 111, 84, 0.2);
            border-radius: 2px;
        }

        /* 모달 애니메이션 */
        .modal-overlay {
            background-color: rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(4px);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.95); }
            to { opacity: 1; transform: scale(1); }
        }
        .animate-modal { animation: fadeIn 0.2s ease-out; }

        /* 모바일 스티키 비디오 레이아웃 */
        @media (max-width: 1023px) {
            .sticky-video-container {
                position: sticky;
                top: 60px;
                z-index: 40;
            }
        }
    </style>
</head>
<body>
    <div id="root"></div>

    <script type="text/babel">
        const { useState, useRef, useEffect, useMemo } = React;

        const Icon = ({ name, size = 20, className = "" }) => {
            const icons = {
                play: <polygon points="5 3 19 12 5 21 5 3"></polygon>,
                pause: <><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></>,
                sun: <><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></>,
                moon: <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>,
                settings: <><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></>,
                search: <><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></>,
                list: <><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></>,
                anchor: <path d="M12 22v-5m0-10V2m0 5a5 5 0 0 1 5 5 5 5 0 0 1-5 5 5 5 0 0 1-5-5 5 5 0 0 1 5-5z"></path>,
                x: <line x1="18" y1="6" x2="6" y2="18"></line>,
                sliders: <><line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line><line x1="2" y1="14" x2="6" y2="14"></line><line x1="10" y1="8" x2="14" y2="8"></line><line x1="18" y1="16" x2="22" y2="16"></line></>,
                mouse: <path d="M3 3l7.07 16.97 2.51-7.39 7.39-2.51L3 3z M13 13l6 6"></path>,
                type: <><polyline points="4 7 4 4 20 4 20 7"></polyline><line x1="12" y1="4" x2="12" y2="20"></line><line x1="9" y1="20" x2="15" y2="20"></line></>,
            };
            return (
                <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
                    {icons[name] || null}
                </svg>
            );
        };

        const App = () => {
            const [videoUrl, setVideoUrl] = useState("https://www.w3schools.com/html/mov_bbb.mp4");
            const [inputUrl, setInputUrl] = useState("");
            const [currentTime, setCurrentTime] = useState(0);
            const [duration, setDuration] = useState(0);
            const [isPlaying, setIsPlaying] = useState(false);
            const [playbackRate, setPlaybackRate] = useState(1.0); 
            
            const [activeIdxKo, setActiveIdxKo] = useState(-1);
            const [activeIdxEn, setActiveIdxEn] = useState(-1);
            const [activeIdxZh, setActiveIdxZh] = useState(-1);
            
            const [anchorLang, setAnchorLang] = useState('ko');
            const [showKo, setShowKo] = useState(true);
            const [showZh, setShowZh] = useState(true);
            const [showEn, setShowEn] = useState(true);
            const [showPinyin, setShowPinyin] = useState(true);
            const [isDarkMode, setIsDarkMode] = useState(false);
            const [showGlobalSettings, setShowGlobalSettings] = useState(false);
            const [clickBehavior, setClickBehavior] = useState('play'); 
            const [searchTerm, setSearchTerm] = useState("");
            
            const [fontSizeKo, setFontSizeKo] = useState(26);
            const [fontSizeZh, setFontSizeZh] = useState(26);
            const [fontSizeEn, setFontSizeEn] = useState(22);

            const [scriptSizeKo, setScriptSizeKo] = useState(16);
            const [scriptSizeZh, setScriptSizeZh] = useState(16);
            const [scriptSizeEn, setScriptSizeEn] = useState(14);

            const [loopA, setLoopA] = useState(null);
            const [loopB, setLoopB] = useState(null);
            const [isLooping, setIsLooping] = useState(false);

            const videoRef = useRef(null);
            const scrollRef = useRef(null);

            const multiTracks = {
                ko: [
                    { start: 0, end: 5, text: "안녕하세요! JW Multiple Player 테스트 영상입니다." },
                    { start: 5.1, end: 10, text: "이제 실시간으로 여러 자막을 동시에 확인할 수 있습니다." },
                    { start: 38.6, end: 44.1, text: "성경 사도행전 11장을 펴서 초기 회중의 역사를 보시죠." }
                ],
                zh: [
                    { start: 0, end: 5, text: "你好！ 这是 JW Multiple Player 测试视频。", pinyin: "Nǐ hǎo! Zhè shì JW Multiple Player cèshì shìpín." },
                    { start: 5.1, end: 10, text: "现在您可以同时查看多个字幕。", pinyin: "Xiànzài nín kěyǐ tóngshí chákàn duō gè zìmù." },
                    { start: 38.5, end: 44.2, text: "请翻开圣经 使徒行传11章, 这里记录了会众早期的历史,", pinyin: "Qǐng fānkāi Shèngjīng Shǐtú Xíngzhuàn 11 zhāng..." }
                ],
                en: [
                    { start: 0, end: 5, text: "Hello! This is a test video for JW Multiple Player." },
                    { start: 5.1, end: 10, text: "Now you can check multiple subtitles simultaneously." },
                    { start: 38.4, end: 44.3, text: "Well, let’s open our Bibles to Acts chapter 11." }
                ]
            };

            const togglePlay = () => {
                if (!videoRef.current) return;
                if (videoRef.current.paused) { videoRef.current.play(); setIsPlaying(true); } 
                else { videoRef.current.pause(); setIsPlaying(false); }
            };

            const handleTimeUpdate = () => {
                if (!videoRef.current) return;
                const time = videoRef.current.currentTime;
                setCurrentTime(time);
                if (isLooping && loopA !== null && loopB !== null && time >= loopB) { videoRef.current.currentTime = loopA; }
                setActiveIdxKo(multiTracks.ko.findIndex(it => time >= it.start && time < it.end));
                setActiveIdxEn(multiTracks.en.findIndex(it => time >= it.start && time < it.end));
                setActiveIdxZh(multiTracks.zh.findIndex(it => time >= it.start && time < it.end));
            };

            const handleRateChange = (rate) => {
                setPlaybackRate(rate);
                if (videoRef.current) videoRef.current.playbackRate = rate;
            };

            const seekTo = (sec) => {
                if (!videoRef.current) return;
                videoRef.current.currentTime = sec;
                if (clickBehavior === 'play') { videoRef.current.play(); setIsPlaying(true); } 
                else { videoRef.current.pause(); setIsPlaying(false); }
            };

            const highlightText = (text, queries) => {
                if (!queries || queries.length === 0 || !text) return text;
                const pattern = queries.map(q => q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|');
                const parts = text.split(new RegExp(`(${pattern})`, 'gi'));
                return parts.map((part, i) => 
                    queries.some(q => q.toLowerCase() === part.toLowerCase()) ? 
                    <mark key={i} className="bg-emerald-100 dark:bg-emerald-900/50 text-emerald-900 dark:text-emerald-100 rounded-sm px-0.5 font-bold transition-colors">{part}</mark> : part
                );
            };

            const searchWords = useMemo(() => searchTerm.trim().split(/\s+/).filter(w => w.length > 0), [searchTerm]);

            const anchorList = useMemo(() => {
                const leadTrack = multiTracks[anchorLang];
                return leadTrack.map((leadItem, idx) => {
                    const midTime = (leadItem.start + leadItem.end) / 2;
                    const findMatched = (track) => track.find(it => midTime >= it.start && midTime < it.end) || track.find(it => leadItem.start >= it.start && leadItem.start < it.end);
                    return {
                        id: idx,
                        start: leadItem.start,
                        end: leadItem.end,
                        ko: anchorLang === 'ko' ? leadItem.text : findMatched(multiTracks.ko)?.text || "",
                        zh: anchorLang === 'zh' ? leadItem.text : findMatched(multiTracks.zh)?.text || "",
                        pinyin: anchorLang === 'zh' ? leadItem.pinyin : findMatched(multiTracks.zh)?.pinyin || "",
                        en: anchorLang === 'en' ? leadItem.text : findMatched(multiTracks.en)?.text || ""
                    };
                });
            }, [anchorLang]);

            const filteredList = useMemo(() => {
                if (searchWords.length === 0) return anchorList;
                return anchorList.filter(it => {
                    const combined = `${it.ko} ${it.zh} ${it.en} ${it.pinyin}`.toLowerCase();
                    return searchWords.every(word => combined.includes(word.toLowerCase()));
                });
            }, [anchorList, searchWords]);

            useEffect(() => {
                const leadIdx = anchorLang === 'ko' ? activeIdxKo : anchorLang === 'zh' ? activeIdxZh : activeIdxEn;
                if (leadIdx !== -1 && scrollRef.current && searchWords.length === 0) {
                    const el = scrollRef.current.children[leadIdx];
                    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }, [activeIdxKo, activeIdxZh, activeIdxEn, anchorLang, searchWords]);

            const themeClass = isDarkMode ? "bg-slate-950 text-slate-300 dark" : "bg-slate-100 text-slate-700 light";
            const cardClass = isDarkMode ? "bg-slate-900/60 border-white/5 shadow-2xl" : "bg-white border-slate-200 shadow-xl";
            const buttonAccent = isDarkMode ? "bg-[#2d8a6e] hover:bg-[#1E6F54]" : "bg-[#1E6F54] hover:bg-[#154d3a]";
            const accentText = isDarkMode ? "text-[#34a87e]" : "text-[#1E6F54]";

            return (
                <div className={`min-h-screen font-sans flex flex-col ${themeClass}`}>
                    
                    {/* --- GLOBAL HEADER --- */}
                    <nav className={`h-[60px] border-b px-4 lg:px-8 flex items-center justify-between sticky top-0 backdrop-blur-xl z-50 ${isDarkMode ? 'bg-slate-950/80 border-white/5' : 'bg-white/80 border-slate-200 shadow-sm'}`}>
                        <div className="flex items-center gap-4">
                            <div className={`w-9 h-9 ${buttonAccent} rounded-xl flex items-center justify-center font-black text-white`}>MP</div>
                            <h1 className={`font-black text-sm lg:text-base ${accentText} leading-none uppercase tracking-tighter`}>JW Player Pro</h1>
                        </div>
                        
                        <div className="flex items-center gap-2 lg:gap-4 flex-1 max-w-lg mx-4">
                            <div className="relative w-full">
                                <Icon name="search" className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={14} />
                                <input type="text" placeholder="URL 입력..." className={`w-full pl-9 pr-4 py-2 rounded-xl border text-xs outline-none ${isDarkMode ? 'bg-slate-900 border-white/5' : 'bg-slate-50 border-slate-200'}`} value={inputUrl} onChange={(e) => setInputUrl(e.target.value)} />
                            </div>
                            <button onClick={() => setVideoUrl(inputUrl)} className={`px-4 py-2 ${buttonAccent} text-white text-[10px] font-bold rounded-xl shrink-0`}>로드</button>
                        </div>

                        <div className="flex items-center gap-2">
                            <button onClick={() => setShowGlobalSettings(true)} className={`p-2 rounded-xl border ${isDarkMode ? 'bg-slate-900 text-slate-400' : 'bg-white text-slate-500 shadow-sm'}`}>
                                <Icon name="settings" size={20} />
                            </button>
                            <button onClick={() => setIsDarkMode(!isDarkMode)} className={`p-2 rounded-xl border ${isDarkMode ? 'bg-slate-900 text-yellow-500' : 'bg-white text-slate-500 shadow-sm'}`}>
                                <Icon name={isDarkMode ? "sun" : "moon"} size={20} />
                            </button>
                        </div>
                    </nav>

                    {/* --- MAIN CONTENT: 6:4 Ratio --- */}
                    <main className="max-w-[1600px] mx-auto p-4 lg:p-8 grid grid-cols-1 lg:grid-cols-10 gap-6 lg:gap-10 flex-1 w-full overflow-hidden">
                        
                        {/* --- LEFT: VIDEO AREA (6) --- */}
                        <div className="lg:col-span-6 flex flex-col gap-6 sticky-video-container">
                            {/* Video Container (Photo 1 Style) */}
                            <div className={`aspect-video rounded-[2rem] lg:rounded-[3rem] overflow-hidden shadow-2xl relative border-4 ${isDarkMode ? 'bg-black border-slate-900' : 'bg-white border-white'}`}>
                                <video key={videoUrl} ref={videoRef} onClick={togglePlay} className="w-full h-full object-contain cursor-pointer" onTimeUpdate={handleTimeUpdate} onLoadedMetadata={(e) => setDuration(e.target.duration)} playsInline>
                                    <source src={videoUrl} type="video/mp4" />
                                </video>
                                
                                {/* Subtitle Overlay */}
                                <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/90 via-black/10 to-transparent p-6 lg:p-12 text-center pointer-events-none flex flex-col items-center justify-end min-h-[50%]">
                                    <div className="space-y-2 flex flex-col items-center w-full">
                                        {showKo && activeIdxKo !== -1 && <p className="font-black text-white drop-shadow-[0_4px_4px_rgba(0,0,0,1)]" style={{ fontSize: `${fontSizeKo}px` }}>{multiTracks.ko[activeIdxKo].text}</p>}
                                        {showZh && activeIdxZh !== -1 && (
                                            <div className="flex flex-col items-center">
                                                {showPinyin && <span className="px-3 py-1 mb-2 bg-emerald-600/70 text-emerald-50 font-mono rounded-lg shadow-xl text-sm" style={{ fontSize: `${fontSizeZh * 0.6}px` }}>{multiTracks.zh[activeIdxZh].pinyin}</span>}
                                                <p className="text-emerald-300 font-bold drop-shadow-[0_4px_4px_rgba(0,0,0,1)]" style={{ fontSize: `${fontSizeZh}px` }}>{multiTracks.zh[activeIdxZh].text}</p>
                                            </div>
                                        )}
                                        {showEn && activeIdxEn !== -1 && <p className="text-slate-200 font-medium drop-shadow-[0_4px_4px_rgba(0,0,0,1)]" style={{ fontSize: `${fontSizeEn}px` }}>{multiTracks.en[activeIdxEn].text}</p>}
                                    </div>
                                </div>
                            </div>

                            {/* Internal Playback Controls (Photo 2 Style) */}
                            <div className={`p-6 rounded-[2.5rem] border-2 flex flex-col gap-6 ${cardClass}`}>
                                <div className="flex items-center gap-6">
                                    <button onClick={togglePlay} className={`w-16 h-16 ${buttonAccent} text-white rounded-[1.5rem] flex items-center justify-center shadow-lg shrink-0 transition-transform active:scale-95`}>
                                        <Icon name={isPlaying ? "pause" : "play"} size={32} />
                                    </button>
                                    <div className="flex-1">
                                        <div className="flex justify-between items-end mb-2">
                                            <span className="text-[10px] font-black uppercase tracking-widest opacity-40">Playing Now</span>
                                            <span className="text-xs font-mono font-bold opacity-60">{Math.floor(currentTime)}s / {Math.floor(duration)}s</span>
                                        </div>
                                        <div className={`h-3 rounded-full relative overflow-hidden cursor-pointer ${isDarkMode ? 'bg-white/10' : 'bg-slate-100 shadow-inner'}`} onClick={(e) => {
                                            const rect = e.currentTarget.getBoundingClientRect();
                                            seekTo(((e.clientX - rect.left) / rect.width) * duration);
                                        }}>
                                            <div className="h-full bg-[#1E6F54] transition-all" style={{ width: `${(currentTime / (duration || 1)) * 100}%` }} />
                                        </div>
                                    </div>
                                </div>

                                {/* Stacked Controls: Speed & Loop */}
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    <div className="space-y-3">
                                        <div className="flex justify-between text-[10px] font-black uppercase opacity-40">Speed <span className="text-emerald-600">{playbackRate}x</span></div>
                                        <div className={`flex p-1 rounded-xl border ${isDarkMode ? 'bg-slate-950 border-white/5' : 'bg-slate-50 border-slate-200'}`}>
                                            {[0.8, 1.0, 1.2, 1.5].map(rate => (
                                                <button key={rate} onClick={() => handleRateChange(rate)} className={`flex-1 py-2 rounded-lg text-xs font-black transition-all ${playbackRate === rate ? 'bg-[#1E6F54] text-white shadow-md' : 'text-slate-400 hover:text-emerald-600'}`}>{rate}x</button>
                                            ))}
                                        </div>
                                    </div>
                                    <div className="space-y-3">
                                        <div className="flex justify-between text-[10px] font-black uppercase opacity-40">A-B Loop <span className={isLooping ? 'text-emerald-600 font-black' : 'opacity-40'}>{isLooping ? 'ON' : 'OFF'}</span></div>
                                        <div className="flex gap-2">
                                            <button onClick={() => setLoopA(currentTime)} className={`flex-1 py-2 rounded-lg text-[10px] font-black border transition-all ${loopA !== null ? 'bg-emerald-100 text-emerald-700 border-emerald-200' : 'bg-slate-50 dark:bg-slate-800 text-slate-400 border-transparent'}`}>{loopA !== null ? `A: ${Math.floor(loopA)}s` : 'Start A'}</button>
                                            <button onClick={() => setLoopB(currentTime)} className={`flex-1 py-2 rounded-lg text-[10px] font-black border transition-all ${loopB !== null ? 'bg-emerald-100 text-emerald-700 border-emerald-200' : 'bg-slate-50 dark:bg-slate-800 text-slate-400 border-transparent'}`}>{loopB !== null ? `B: ${Math.floor(loopB)}s` : 'End B'}</button>
                                            <button onClick={() => setIsLooping(!isLooping)} disabled={loopA === null || loopB === null} className={`px-4 rounded-lg transition-all ${isLooping ? 'bg-emerald-600 text-white shadow-md' : 'bg-slate-200 dark:bg-slate-800 text-slate-400 opacity-50'}`}><Icon name="anchor" size={18}/></button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* --- RIGHT: SCRIPT AREA (4) --- */}
                        <div className={`lg:col-span-4 flex flex-col rounded-[2.5rem] border-2 overflow-hidden h-[85vh] ${cardClass}`}>
                            <div className={`p-6 border-b border-slate-200 dark:border-white/5 flex flex-col gap-5 ${isDarkMode ? 'bg-white/5' : 'bg-slate-50/50'}`}>
                                <div className="flex items-center justify-between">
                                    <h3 className={`font-black text-lg flex items-center gap-2 ${isDarkMode ? 'text-white' : 'text-slate-700'}`}><Icon name="list" size={22} className={accentText} /> Script</h3>
                                    <div className={`flex p-1 rounded-xl border ${isDarkMode ? 'bg-slate-900 border-white/5' : 'bg-white border-slate-200 shadow-sm'}`}>
                                        {['ko','zh','en'].map(l => (
                                            <button key={l} onClick={() => setAnchorLang(l)} className={`px-4 py-1.5 rounded-lg text-[10px] font-black transition-all ${anchorLang === l ? 'bg-[#1E6F54] text-white shadow-md' : 'text-slate-400 hover:text-emerald-600'}`}>{l.toUpperCase()}</button>
                                        ))}
                                    </div>
                                </div>
                                <div className="relative">
                                    <Icon name="search" className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
                                    <input type="text" placeholder="스크립트 검색..." className={`w-full pl-12 pr-4 py-3 rounded-2xl border text-sm outline-none transition-all focus:ring-2 focus:ring-emerald-500/20 ${isDarkMode ? 'bg-slate-900 border-white/5 text-white' : 'bg-white border-slate-200 shadow-sm text-slate-700'}`} value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} />
                                </div>
                            </div>

                            <div ref={scrollRef} className="flex-1 overflow-y-auto p-6 space-y-4 custom-scrollbar">
                                {filteredList.length > 0 ? (
                                    filteredList.map((item, index) => {
                                        const isActive = (anchorLang === 'ko' && activeIdxKo === index) || (anchorLang === 'zh' && activeIdxZh === index) || (anchorLang === 'en' && activeIdxEn === index);
                                        return (
                                            <div key={index} onClick={() => seekTo(item.start)} className={`p-6 rounded-[2rem] cursor-pointer transition-all border-2 relative overflow-hidden group ${isActive && searchWords.length === 0 ? 'bg-[#1E6F54]/10 border-[#1E6F54] ring-2 ring-emerald-500/10' : isDarkMode ? 'bg-slate-900/40 border-transparent hover:border-white/10 shadow-lg' : 'bg-white border-slate-100 hover:border-[#1E6F54]/20 hover:shadow-xl'}`}>
                                                <div className="flex justify-between items-center mb-4">
                                                    <span className={`text-[10px] font-mono px-3 py-1 rounded-lg font-black ${isActive ? 'bg-[#1E6F54] text-white' : 'bg-slate-100 dark:bg-slate-800 text-slate-400'}`}>{Math.floor(item.start)}s</span>
                                                    <Icon name="mouse" size={14} className={`opacity-0 group-hover:opacity-30 transition-opacity ${accentText}`} />
                                                </div>
                                                <div className="space-y-4">
                                                    {showKo && item.ko && <p className={`leading-snug transition-all ${isActive ? accentText + ' font-black' : 'opacity-80'}`} style={{ fontSize: `${scriptSizeKo}px` }}>{highlightText(item.ko, searchWords)}</p>}
                                                    {showZh && item.zh && (
                                                        <div className="space-y-2">
                                                            {showPinyin && item.pinyin && <span className={`px-2 py-0.5 font-mono text-xs rounded-md ${isActive ? 'bg-[#1E6F54]/10 text-emerald-600' : 'text-slate-400'}`} style={{ fontSize: `${scriptSizeZh * 0.7}px` }}>{highlightText(item.pinyin, searchWords)}</span>}
                                                            <p className={`leading-relaxed font-bold ${isActive ? 'text-emerald-500' : 'opacity-70'}`} style={{ fontSize: `${scriptSizeZh}px` }}>{highlightText(item.zh, searchWords)}</p>
                                                        </div>
                                                    )}
                                                    {showEn && item.en && <p className={`leading-relaxed transition-all ${isActive ? 'text-slate-900 dark:text-slate-100' : 'opacity-40 italic'}`} style={{ fontSize: `${scriptSizeEn}px` }}>{highlightText(item.en, searchWords)}</p>}
                                                </div>
                                            </div>
                                        );
                                    })
                                ) : (
                                    <div className="text-center py-20 opacity-30 italic font-black">No Results Found</div>
                                )}
                            </div>
                        </div>
                    </main>

                    {/* --- GLOBAL SETTINGS MODAL (Photo 3 Style) --- */}
                    {showGlobalSettings && (
                        <div className="fixed inset-0 z-[100] flex items-center justify-center p-4 modal-overlay" onClick={() => setShowGlobalSettings(false)}>
                            <div className={`w-full max-w-lg rounded-[2.5rem] p-8 shadow-2xl animate-modal ${isDarkMode ? 'bg-slate-900 border border-white/10' : 'bg-white border border-slate-200'}`} onClick={e => e.stopPropagation()}>
                                <div className="flex justify-between items-center mb-8">
                                    <h2 className="text-2xl font-black tracking-tight flex items-center gap-3"><Icon name="settings" size={24} className={accentText} /> Preferences</h2>
                                    <button onClick={() => setShowGlobalSettings(false)} className="p-2 hover:bg-slate-100 dark:hover:bg-white/5 rounded-full"><Icon name="x" size={20} /></button>
                                </div>

                                <div className="space-y-8">
                                    {/* Subtitle Toggles */}
                                    <div className="space-y-4">
                                        <label className="text-xs font-black uppercase tracking-widest opacity-40">Subtitle Visibility</label>
                                        <div className={`flex p-2 rounded-2xl border ${isDarkMode ? 'bg-slate-950 border-white/5 shadow-inner' : 'bg-slate-50 border-slate-200'}`}>
                                            {[
                                                {id: 'KO', state: showKo, set: setShowKo},
                                                {id: 'ZH', state: showZh, set: setShowZh},
                                                {id: 'EN', state: showEn, set: setShowEn}
                                            ].map(l => (
                                                <button key={l.id} onClick={() => l.set(!l.state)} className={`flex-1 py-3 rounded-xl text-xs font-black transition-all ${l.state ? 'bg-[#1E6F54] text-white shadow-lg' : 'text-slate-400 opacity-60'}`}>{l.id}</button>
                                            ))}
                                        </div>
                                        <button onClick={() => setShowPinyin(!showPinyin)} className={`w-full py-3 rounded-xl text-xs font-black border transition-all ${showPinyin ? 'bg-emerald-100 text-emerald-700 border-emerald-200' : 'text-slate-400 opacity-40 border-transparent'}`}>ZH Pinyin Toggle</button>
                                    </div>

                                    {/* Font Size Sliders */}
                                    <div className="space-y-6">
                                        <label className="text-xs font-black uppercase tracking-widest opacity-40">Font Size (Video Overlay)</label>
                                        <div className="space-y-5">
                                            {[
                                                {label: 'KO', val: fontSizeKo, set: setFontSizeKo},
                                                {label: 'ZH', val: fontSizeZh, set: setFontSizeZh},
                                                {label: 'EN', val: fontSizeEn, set: setFontSizeEn}
                                            ].map((l, i) => (
                                                <div key={i} className="flex items-center gap-6">
                                                    <span className="text-xs font-black opacity-50 w-8">{l.label}</span>
                                                    <input type="range" min="14" max="80" value={l.val} onChange={(e) => l.set(Number(e.target.value))} className="flex-1" />
                                                    <span className="text-xs font-mono opacity-40 w-6 text-right">{l.val}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="space-y-6">
                                        <label className="text-xs font-black uppercase tracking-widest opacity-40">Script Click Behavior</label>
                                        <div className={`flex p-1.5 rounded-2xl border ${isDarkMode ? 'bg-slate-950 border-white/5' : 'bg-slate-50 border-slate-200'}`}>
                                            <button onClick={() => setClickBehavior('play')} className={`flex-1 py-2 rounded-xl text-[10px] font-black transition-all ${clickBehavior === 'play' ? 'bg-[#1E6F54] text-white' : 'text-slate-400'}`}>Move & Play</button>
                                            <button onClick={() => setClickBehavior('pause')} className={`flex-1 py-2 rounded-xl text-[10px] font-black transition-all ${clickBehavior === 'pause' ? 'bg-[#1E6F54] text-white' : 'text-slate-400'}`}>Move & Pause</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* --- FOOTER --- */}
                    <footer className={`h-[40px] px-8 border-t flex items-center justify-between text-[10px] font-black uppercase tracking-widest ${isDarkMode ? 'bg-slate-950 text-slate-700 border-white/5' : 'bg-white text-slate-300 border-slate-200'}`}>
                        <span>JW Multiple Player Pro v6.0</span>
                        <span className="opacity-50 tracking-tighter">6:4 Golden Layout Active</span>
                    </footer>
                </div>
            );
        };

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
