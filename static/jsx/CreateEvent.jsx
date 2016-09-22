'use strict';
import {bindActionCreators} from 'redux';
import React from 'react';
import ReactDOM from 'react-dom';
import moment from 'moment';
import DatePicker from 'react-datepicker';

let CreateEventView = React.createClass({
  getInitialState: function () {
    return {
      date: null,
    };
  },

  handleDateChange(date) {
    this.setState({
      date: date
    });
  },


  submit() {
    const tags = this.refs.tags.value.split('#');
    if ($('#event-form').valid()) {
      let hour = parseInt(this.refs.hour.value);
      let min = parseInt(this.refs.min.value);
      if (this.refs.time.value == 'PM' && hour != 12) {
        hour = 12 + hour
      }
      let dateTime = this.state.date.set('hour', hour).set('minute', min).format("YYYY-MM-DD HH:mm");
      let serializeTags = [];
      tags.forEach((tag) => {
        if (tag != "") {
          serializeTags.push({'name': tag})
        }
      });

      const data = {
        title: this.refs.title.value,
        location: this.refs.location.value,
        dateTime: dateTime,
        tags: serializeTags
      };
      $.ajax({
        type: "PUT",
        url: '/api/v1/event/create/',
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function (json) {
          console.log(json)
        }
      });
    }

  },

  componentDidMount() {
    const input = this.refs.location;
    const options = {componentRestrictions: {country: 'us'}};

    new google.maps.places.Autocomplete(input, options);
    $(document).on('submit', function (e) {
      e.preventDefault();
    });

    $('#event-form').validate({
      errorPlacement: function (error, element) {
        element.css({"border-color": "red", "border-weight": "1px"});
      }
    });

  },

  render() {
    return (
      <div >
        <h1 className="event-title">Create an Event</h1>
        <br/>
        <form role="form" id="event-form">
          <div className="form-group">
            <label htmlFor="title">Name</label>
            <input maxLength="50" className="form-control" type="text" ref="title" name="title"
                   placeholder="Event Name" required/>
          </div>
          <div className="form-group">
            <label htmlFor="location">Location</label>
            <input type="text" maxLength="120" className="form-control" ref="location" name="location"
                   placeholder="Address" required/>
          </div>
          <div className="form-group">
            <label htmlFor="date" className="">Date</label>
            <label htmlFor="date" className="col-xs-offset-4">Time</label>
            <div className="row">
              <div className="col-xs-4">
                <DatePicker minDate={moment()} selected={this.state.date} onChange={this.handleDateChange}
                            placeholderText="Click to select a date" name="date"
                            isClearable={true} className="form-control" showTodayButton={'Today'} required/>
              </div>
              <div className="col-xs-3">
                <select className="form-control" ref="hour" name="hour" required>
                  <option value={null}/>
                  <option value="1">1</option>
                  <option value="2">2</option>
                  <option value="3">3</option>
                  <option value="4">4</option>
                  <option value="5">5</option>
                  <option value="6">6</option>
                  <option value="7">7</option>
                  <option value="8">8</option>
                  <option value="9">9</option>
                  <option value="10">10</option>
                  <option value="11">11</option>
                  <option value="12">12</option>
                </select>
              </div>
              <div className="col-xs-3">
                <select className="form-control" ref="min" name="min" required>
                  <option value=""/>
                  <option value="0">0</option>
                  <option value="15">15</option>
                  <option value="30">30</option>
                  <option value="45">45</option>
                </select>
              </div>
              <div className="col-xs-2">
                <select className="form-control" ref="time" name="time" required>
                  <option value=""/>
                  <option value="AM">AM</option>
                  <option value="PM">PM</option>
                </select>
              </div>
            </div>
          </div>
          <div className="form-group">
            <label htmlFor="cat">Tags</label>
            <textarea type="text" maxLength="500" className="form-control" ref="tags"
                      placeholder="Enter tags with space and # in front of it" name="tags"/>
          </div>
          <div className="text-center">
            <button type="submit" className="btn btn-success" onClick={this.submit}>Submit</button>
          </div>
        </form>
      </div>
    )
  }
});


ReactDOM.render(
  <CreateEventView />,
  document.getElementById('create-event-jsx'));