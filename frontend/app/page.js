'use client';
import AutocompleteSearch from "@/components/searchbar";
import Results from "@/components/results";
import {useEffect, useState} from "react";
import Progress from "@/components/progress";

export default function Home() {
    const [results, setResults] = useState([]);
    const [viewProgress, setViewProgress] = useState(false);
    const [user, setUser] = useState("");
    useEffect(() => {
        setUser(localStorage.getItem("username"));
    }, []);
    const viewProgressHandler = (view) => {
        setViewProgress(view);
    }
    return (
        <>
            {!viewProgress && <AutocompleteSearch setResults={setResults} viewProgressHandler={viewProgressHandler} />}
            {!viewProgress && results.length > 0 &&  <Results results={results}/>}
            {viewProgress && <Progress viewProgress={viewProgress} viewProgressHandler={viewProgressHandler} user={user}/>}
        </>
    );
}
