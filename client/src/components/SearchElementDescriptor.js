import React, {useState, useEffect} from 'react' 
import "../styles/SearchElement.css"
import "../styles/SearchElementDescriptor.css"

function SearchElementDescriptor()
{
    return( 
    <div className='SearchContainer'>
        <div className='WestCoast'><p>Article Link</p></div>
        <div className='EastCoast'><p>accuracy</p></div>
    </div>

    );
}
export default SearchElementDescriptor