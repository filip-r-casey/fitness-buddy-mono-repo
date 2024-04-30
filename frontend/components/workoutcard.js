import Card from "@mui/material/Card";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import Divider from "@mui/material/Divider";
import Chip from "@mui/material/Chip";
import Button from "@mui/material/Button";
import React, {useState, useRef, useEffect} from "react";
import TextField from "@mui/material/TextField";
import {Alert, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle} from "@mui/material";
import SignIn from "@/components/signin";

// import process from "next/dist/build/webpack/loaders/resolve-url-loader/lib/postcss";

function WorkoutCard({workout}) {
    const environment = process.env.NEXT_PUBLIC_ENVIRONMENT;
    let api_url = ""
    if (environment === "DEV") {
        api_url = process.env.NEXT_PUBLIC_DEV_API;
    } else {
        api_url = process.env.NEXT_PUBLIC_PROD_API;
    }
    const [isFlipped, setIsFlipped] = useState(false);
    const [isFrontVisible, setIsFrontVisible] = useState(true);
    const [transitionTimeout, setTransitionTimeout] = useState(0);
    const [formValues, setFormValues] = useState({
        reps: '',
        sets: ''
    });
    const [isSignInOpen, setIsSignInOpen] = useState(false);
    const [user, setUser] = useState(localStorage.getItem("username"));
    const [reps, setReps] = useState("");
    const [sets, setSets] = useState("");
    const [submitSuccess, setSubmitSuccess] = useState(false);

    useEffect(() => {
        const handleStorageChange = () => {
          const savedUser = localStorage.getItem("username");
          console.log("storage changed");
          setUser(savedUser);
        };

        window.addEventListener("storage", handleStorageChange);

        return () => {
            window.removeEventListener("storage", handleStorageChange);
        }
    }, []);

    const handleFlip = () => {

        clearTimeout(transitionTimeout);
        const timeout = setTimeout(() => {
            flipDone(!isFlipped);
        }, 400);

        setIsFlipped(prevState => !prevState);
        setTransitionTimeout(timeout);
    };

    const setUserSignIn = (username) => {
        setUser(username);
    }

    const flipDone = (flip_status) => {
        if (flip_status) {
            setIsFrontVisible(false);
        } else {
            setIsFrontVisible(true);
        }
    };

    const handleSubmit = () => {
        if (user) {
            handleProgress().then((status) => {
                if (status === 201) {
                    setSubmitSuccess(true);
                } else {
                    setSubmitSuccess(false);
                }
            });
        } else {
            handleOpenSignIn();
        }
    };

    const handleOpenSignIn = () => {
        setIsSignInOpen(true);
    }

    const handleProgress = async () => {
        const exercise_date = new Date();
        const timestamp = exercise_date.getTime() / 1000;
        try {
            const response = await fetch(api_url + 'api/add_progress/', {
                method: "POST",
                headers: {
                    "content-type": "application/json",
                },
                body: JSON.stringify({
                    exercise: workout.name,
                    date: timestamp,
                    sets_completed: sets,
                    reps_completed: reps,
                    user: user
                }),
            });
            return response.status;
        } catch (error) {
            return error.response.status;
        }
    }

    // const handleTransitionEnd = (event) => {
    //     if (event.propertyName === "transform") {
    //         flipDone();
    //     }
    // };

    return (
        <React.Fragment>
            <Card
                className={`mb-5`}
                variant="outlined"
                sx={{
                    maxWidth: 600,
                    minWidth: 400,
                    position: "relative",
                    perspective: "1000px",
                    transition: "transform 0.8s",
                    transformStyle: "preserve-3d",
                    height: "100%",
                }}
                style={{
                    transform: isFlipped ? "rotateY(180deg)" : "rotateY(0deg)",
                    height: "100%"
                }}
                key={workout.name}
                // onTransitionEnd={handleTransitionEnd}
            >
                <div
                    className={`front${isFrontVisible ? "" : " hidden"}`}
                    style={{backfaceVisibility: "hidden", width: "100%", height: "100%"}}
                >
                    <Box sx={{p: 2}}>
                        <Stack direction="row" justifyContent="space-between" alignItems="center">
                            <Typography gutterBottom variant="h5" component="div">
                                {workout.name}
                            </Typography>
                            <Typography gutterBottom variant="h6" component="div">
                                {workout.difficulty}
                            </Typography>
                        </Stack>
                        <Typography color="text.secondary" variant="body2">
                            {workout.instructions}
                        </Typography>
                    </Box>
                    <Divider/>
                    <Box sx={{p: 2}}>
                        <Stack
                            direction={"row"}
                            spacing={2}
                            justifyContent={"space-between"}
                            alignItems={"center"}
                        >
                            <Stack direction="row" spacing={1}>
                                <Chip label={workout.muscle} size="small"/>
                                <Chip label={workout.type} size="small"/>
                                <Chip label={workout.equipment} size="small"/>
                            </Stack>
                            <Button variant={"contained"} id={workout.name.replace(/\s/g, '')} onClick={handleFlip}>
                                Log
                            </Button>
                        </Stack>
                    </Box>
                </div>
                <div
                    className={`back${isFrontVisible ? " hidden" : ""}`}
                    style={{backfaceVisibility: "visible", width: "100%", height: "100%", transform: "rotateY(180deg)"}}
                >
                    <Box className={"w-full"} sx={{p: 2}}>
                        <Stack direction="row" justifyContent="space-between" alignItems="center">
                            <Typography className={"mr-200"} gutterBottom variant="h5" component="div">
                                {`${workout.name}`}
                            </Typography>
                            <Typography gutterBottom variant="h6" component="div">
                                {workout.difficulty}
                            </Typography>
                        </Stack>
                        <Stack className={"width-full"} direction={"column"}>
                            <TextField className={"mb-5"} label="Reps" variant="outlined" value={reps}
                                       onChange={(e) => setReps(e.target.value)}/>
                            <TextField className={"mb-5"} label="Sets" variant="outlined" value={sets}
                                       onChange={(e) => setSets(e.target.value)}/>
                            <Alert className={submitSuccess ? "" : "hidden"} severity="success">
                                Progress Saved
                            </Alert>
                        </Stack>
                    </Box>
                    <Divider/>
                    <Box sx={{p: 2}}>
                        <Stack
                            direction={"row"}
                            spacing={2}
                            justifyContent={"space-between"}
                            alignItems={"center"}
                        >
                            <Button onClick={() => {
                                handleFlip();
                            }}>
                                Back
                            </Button>
                            <Button variant={"contained"} onClick={() => {
                                handleSubmit();
                            }}>
                                Log
                            </Button>
                        </Stack>
                    </Box>
                </div>
            </Card>
            <SignIn isSignInOpen={isSignInOpen} setIsSignInOpen={setIsSignInOpen} setUserHandler={setUserSignIn}/>
        </React.Fragment>

    )
        ;
}

export default WorkoutCard;
