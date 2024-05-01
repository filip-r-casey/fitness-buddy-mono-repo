import Box from "@mui/material/Box";
import {Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography} from "@mui/material";
import Button from "@mui/material/Button";
import process from "next/dist/build/webpack/loaders/resolve-url-loader/lib/postcss";
import {useEffect, useState} from "react";

function Progress({viewProgress, viewProgressHandler, user}) {
    const [rows, setRows] = useState([]);
    const environment = process.env.NEXT_PUBLIC_ENVIRONMENT;
    let api_url = ""
    if (environment === "DEV") {
        api_url = process.env.NEXT_PUBLIC_DEV_API;
    } else {
        api_url = process.env.NEXT_PUBLIC_PROD_API;
    }
    useEffect(() => {
        getProgress();
    }, [user]);
    const getProgress = () => {
        const baseURL = api_url + "progress";
        const params = {
            username: user
        }
        const queryString = new URLSearchParams(params).toString();
        fetch(`${baseURL}?${queryString}`)
            .then(response => {
                return response.json()
            })
            .then(json => {
                setRows(json);
            })
            .catch(error => {
                console.error(error);
            });
    }
    return (
        <Box className={`${viewProgress ? "" : "hidden"} flex flex-col`}>
            <Button className={"absolute mt-7"} onClick={() => {
                viewProgressHandler(false);
            }}>Back</Button>
            <Typography variant={"h2"} className={"mt-20"}>Your Progress</Typography>
            <div className={"flex"}>
                <div className={"mt-20 ml-5 mr-5 max-w-.5"}>
                    <TableContainer component={Paper}>
                        <Table sx={{minWidth: 650}} aria-label="simple table">
                            <TableHead>
                                <TableRow>
                                    <TableCell align="left">Date</TableCell>
                                    <TableCell align="left">Workout</TableCell>
                                    <TableCell align="left">Reps</TableCell>
                                    <TableCell align="left">Sets</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {rows.map((row) => (
                                    <TableRow
                                        key={row.workout_name + row.date}
                                        sx={{'&:last-child td, &:last-child th': {border: 0}}}
                                        id={row.workout_name + row.date}
                                    >
                                        <TableCell align="left">
                                            {row.date}
                                        </TableCell>
                                        <TableCell align="left">{row.workout_name}</TableCell>
                                        <TableCell align="left">{row.reps}</TableCell>
                                        <TableCell align="left">{row.sets}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </div>
            </div>
        </Box>
    )
}

export default Progress;