import React from 'react';
import {Card} from "@mui/material";
import Box from '@mui/material/Box';
import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import WorkoutCard from "@/components/workoutcard";


function Results({results}) {
    return (
        <div className={"flex flex-col justify-center items-center"}>
            {results.map(workout => (
                <WorkoutCard key={workout.name} workout={workout}/>
            ))}

        </div>
    );
}


// <div className={"flex-1 items-center"}>
//     {results.slice(0,1).map(workout=> (
//         <div key={workout.name}>
//             <h3>{workout.name}</h3>
//             <p>{workout.instructions}</p>
//         </div>
//     ))}
// </div>

export default Results;
