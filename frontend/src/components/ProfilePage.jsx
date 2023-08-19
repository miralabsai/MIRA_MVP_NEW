import React, { useEffect, useState } from "react";
import { DotWave } from '@uiball/loaders';
import "./ProfilePage.css";

function ProfilePage() {
  const [active, setActive] = useState(null);
  const [profile, setProfile] = useState({
    record_id: "",
    username: "",
    email: "",
    firstName: "",
    lastName: "",
  });
  const [loading, setLoading] = useState(false);

  const handleCloseSection = () => {
    setActive(false);
  };

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');

      if (!token) {
        console.error('Token is undefined or not found in local storage');
        setLoading(false);
        return;
      }

      const response = await fetch("http://localhost:8000/users/me/", {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();
      // Log the entire response data to inspect the structure
      console.log('Full profile data:', data);
      if (response.ok) {
        const record_id = data.record_id || ""; // Make sure this matches the field in your response
        if (!record_id) {
          console.error('Record ID not found in the response');
        } else {
          console.log('Fetched record ID:', record_id); // Log the record ID
        }
        const firstName = data.first_name || "";
        const lastName = data.last_name || "";
        const email = data.username || "";

        setProfile({
          record_id: record_id,
          username: data.username,
          email: email,
          firstName: firstName,
          lastName: lastName,
        });

        console.log('id:', record_id); // Print the record ID to debug
      } else {
        console.error('Error fetching profile:', data.detail || 'Unknown error');
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleUpdateProfile = async () => {
    const { record_id, username, first_name, last_name, role, phone_number } = profile;
    const updateUrl = `http://localhost:8000/users/update/${record_id}`;
  
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('Token is undefined or not found in local storage');
      return;
    }
  
    // Debugging logs
    console.log('id:', record_id); // Print the record ID
    console.log('Update URL:', updateUrl); // Print the URL
  
    const updateData = {
      phone_number
      // Add other fields as needed
    };
  
    // Log the data that will be sent to the back end
    console.log('Sending update data:', updateData);
  
    setLoading(true);
    try {
      const response = await fetch(updateUrl, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData),
      });
  
      const data = await response.json();
  
      if (response.ok) {
        console.log('Profile updated successfully:', data); // Log success data
        alert('Profile updated successfully');
      } else {
        console.error('Error updating profile:', data); // Log error data
        alert(data.detail || 'An error occurred while updating the profile.');
      }
     } catch (error) {
        console.error("An error occurred while updating the profile:", error);
        // Handle any additional error logic here, such as showing an alert to the user
    }
    setLoading(false);
  };

  const ProfileIcon = ({ firstName, lastName }) => {
    const initials = `${firstName.charAt(0)}${lastName.charAt(0)}`;
    return <div className="avatar-placeholder">{initials}</div>;
  };

         return (
          <div>
            <button onClick={() => setActive(true)}>Profile</button>
            <div className={`profile-container ${active ? 'active' : ''}`}>
              <button className="close-button" onClick={handleCloseSection}>&times;</button>
              {loading ? (
                <DotWave size={47} speed={1} color="black" />
              ) : (
                <div>
                  <ProfileIcon firstName={profile.firstName} lastName={profile.lastName} />
                  <div>
                    <label>Username:</label>
                    <span>{profile.username}</span>
                  </div>
                  <div>
                    <label>Email:</label>
                    <span>{profile.email}</span>
                  </div>
                  <div>
                    <label>Full Name:</label>
                    <span>{profile.firstName} {profile.lastName}</span>
                  </div>
                  <div>
                    <label>Phone Number:</label>
                    <input
                      type="text"
                      value={profile.phone_number || ""}
                      onChange={(e) => setProfile({ ...profile, phone_number: e.target.value })}
                    />
                  </div>
                  {/* Include other fields for profile picture upload, avatar selection, and other details */}
                  <button className="updatedProfile" onClick={handleUpdateProfile}>Update Profile</button>
                </div>
              )}
            </div>
          </div>
        );
      }
      export default ProfilePage;