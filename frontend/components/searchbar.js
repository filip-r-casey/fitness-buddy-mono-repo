'use client';

import React, {useEffect, useState} from 'react';
import TextField from '@mui/material/TextField';
import Autocomplete from '@mui/material/Autocomplete';
import Button from "@mui/material/Button";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import {IconButton, Tooltip} from "@mui/material";
import SignIn from "@/components/signin";

// import process from "next/dist/build/webpack/loaders/resolve-url-loader/lib/postcss";

function AutocompleteSearch({setResults, viewProgressHandler}) {
    const api_key = process.env.NEXT_PUBLIC_API_NINJA_KEY;
    const requestOptions = {
        method: "GET", headers: {"Content-Type": "application/json", "X-Api-Key": api_key},
    }
    const [submitted, setSubmitted] = useState(false);
    const [user, setUser] = useState("");
    const [showSignIn, setShowSignIn] = useState(false);

    useEffect(() => {
        const user_default = localStorage.getItem("username");
        setUser(user_default);
    }, []);
    const setUserSignIn = (user) => {
        setUser(user);
    }

    const handleSubmit = (event, value) => {
        event.preventDefault();
        fetch(`https://api.api-ninjas.com/v1/exercises?name=${value}`, requestOptions)
            .then(response => response.json())
            .then(json => {
                setResults(json)
            })
            .catch(error => {
                console.error(error);
                setResults([]);
            });
        setSubmitted(true);
    }

    return (<React.Fragment>
            <div className={`flex items-center justify-center min-h-24 mb-10`}>
                <div
                    className={`w-2/3 rounded-lg shadow-lg transition-transform duration-500 ease-in-out ${submitted ? 'translate-top' : 'translate-mid'}`}>
                    <form onSubmit={(e) => handleSubmit(e, document.getElementById('autocomplete-input').value)}
                          className={`w-full ${submitted ? "" : "shadow-xl"}`}>
                        <Autocomplete
                            freeSolo
                            id="autocomplete-input"
                            options={[]}
                            renderInput={(params) => (<TextField
                                {...params}
                                label="What are we doing today?"
                                variant="outlined"
                            />)}
                        />
                    </form>
                </div>
                <Tooltip title={`${user ? user : 'Sign in'}`}>
                    <IconButton
                        size="large"
                        color={user ? "success" : ""}
                        className={"top-8 right-5 absolute"}
                        onClick={() => {
                            if (user) {
                                viewProgressHandler(true);
                            } else {
                                setShowSignIn(true);
                            }

                        }}
                    ><AccountCircleIcon/></IconButton>
                </Tooltip>
            </div>
            <SignIn isSignInOpen={showSignIn} setIsSignInOpen={setShowSignIn} setUserHandler={setUserSignIn}/>
        </React.Fragment>

    );
}

export default AutocompleteSearch;
