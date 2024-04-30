import {Dialog, DialogActions, DialogContent, DialogTitle} from "@mui/material";
import Stack from "@mui/material/Stack";
import Divider from "@mui/material/Divider";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import React from "react";
import process from "next/dist/build/webpack/loaders/resolve-url-loader/lib/postcss";

function SignIn({isSignInOpen, setIsSignInOpen, setUserHandler}) {
    const environment = process.env.NEXT_PUBLIC_ENVIRONMENT;
    let api_url = ""
    if (environment === "DEV") {
        api_url = process.env.NEXT_PUBLIC_DEV_API;
    } else {
        api_url = process.env.NEXT_PUBLIC_PROD_API;
    }
    const handleCloseSignIn = () => setIsSignInOpen(false);
    const handleSignIn = async (event) => {
        event.preventDefault(); // This will prevent the form from submitting traditionally
        const formData = new FormData(event.currentTarget); // Use currentTarget to refer to the form
        const email = formData.get("email");
        const password = formData.get("password");
        console.log("Signing in with", email, password);
        try {
            const response = await fetch(api_url + 'api/sign_in/', {
                method: "POST",
                headers: {
                    "content-type": "application/json",
                },
                body: JSON.stringify({email, password}),
            });

            if (!response.ok) {
                console.error(response);
            } else {
                const data = await response.json();
                localStorage.setItem("username", data.username);
                setUserHandler(data.username);
                console.log("User Signed in");
            }
        } catch (error) {
            console.error(error);
        }
        handleCloseSignIn();
    };

    const handleSignUp = async (event) => {
        event.preventDefault(); // Prevent the default form submission
        const formData = new FormData(event.currentTarget); // Use currentTarget here as well
        const username = formData.get("username");
        const email = formData.get("email");
        const password = formData.get("password");
        const confirmPassword = formData.get("passwordSignUp");

        if (password !== confirmPassword) {
            console.error("Passwords don't match");
            return;
        }
        try {
            const response = await fetch(api_url + 'api/sign_up/', {
                method: "POST",
                headers: {
                    "content-type": "application/json",
                },
                body: JSON.stringify({username, email, password}),
            });

            if (!response.ok) {
                console.error(response);
            } else {
                localStorage.setItem("username", username.toString());
                setUserHandler(username);
                console.log("User Signed in");
            }
        } catch (error) {
            console.error(error);
        }
        handleCloseSignIn();
    };

    return (
        <Dialog
            open={isSignInOpen}
            onClose={handleCloseSignIn}>
            <DialogTitle>Save your workout</DialogTitle>
            <DialogContent>
                <Stack
                    direction="row"
                    justifyContent="space-between"
                    alignItems="center"
                    divider={<Divider orientation={"vertical"} flexItem/>}
                    spacing={2}
                >
                    <Box component="form" className="w-1/2" onSubmit={handleSignIn} noValidate>
                        <Typography variant="h5" gutterBottom>Sign In</Typography>
                        <TextField
                            autoFocus
                            required
                            margin="dense"
                            id="emailSignIn"
                            name="email"
                            label="Email Address"
                            type="email"
                            fullWidth
                            variant="standard"
                        />
                        <TextField
                            required
                            margin="dense"
                            id="passwordSignIn"
                            name="password"
                            label="Password"
                            type="password"
                            fullWidth
                            variant="standard"
                        />
                        <Button type="submit" variant="contained">Sign In</Button>
                    </Box>
                    <Box component="form" className="w-1/2" onSubmit={handleSignUp} noValidate>
                        <Typography variant="h5" gutterBottom>Sign Up</Typography>
                        <TextField
                            required
                            margin="dense"
                            id="nameSignUp"
                            name="username"
                            label="Username"
                            type="name"
                            fullWidth
                            variant="standard"
                        />
                        <TextField
                            required
                            margin="dense"
                            id="emailSignUp"
                            name="email"
                            label="Email"
                            type="email"
                            fullWidth
                            variant="standard"
                        />
                        <TextField
                            required
                            margin="dense"
                            id="passwordSignUp"
                            name="password"
                            label="Password"
                            type="password"
                            fullWidth
                            variant="standard"
                        />
                        <TextField
                            required
                            margin="dense"
                            id="passwordConfirmSignUp"
                            name="passwordSignUp"
                            label="Confirm Password"
                            type="password"
                            fullWidth
                            variant="standard"
                        />
                        <Button type="submit" variant="contained">Sign Up</Button>
                    </Box>
                </Stack>
            </DialogContent>
        </Dialog>
    );
};

export default SignIn;
