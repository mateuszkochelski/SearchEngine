import React, {useState, useEffect} from 'react' 
import "../styles/SearchElement.css"
function SearchElement(props)
{

    return (
        <div className = "SearchContainer">
            <div className = "WestCoast">
                <a href={`https://en.wikipedia.org/wiki/${props.link}`}>{props.link}</a>
            </div>
            <div className = "EastCoast">
                {props.accuracy}
            </div>
        </div>    
    );
}

export default SearchElement