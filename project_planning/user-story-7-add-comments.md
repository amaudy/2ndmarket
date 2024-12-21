# User Story 7: Add Comments to Listing

## Objective
As a logged-in user, I want to be able to add comments to listings so that I can ask questions about the item or provide feedback.

## Prerequisites
- User must be logged in
- Listing must be active
- Listing must exist in the system

## Acceptance Criteria

### Comment Creation
- [ ] Comment form visible only to logged-in users
- [ ] Comment form includes:
  - Text area for comment (max 1000 characters)
  - Submit button
  - Cancel button (if editing)
- [ ] Character counter
- [ ] Preview comment option
- [ ] Submit button enabled only with valid content

### Comment Display
- [ ] Show comments in chronological order (newest first)
- [ ] For each comment show:
  - User avatar/icon
  - Username
  - Comment timestamp
  - Comment text
  - Edit/Delete buttons (for own comments)
- [ ] Pagination or infinite scroll for comments
- [ ] Comment count display

### Comment Management
- [ ] Allow users to edit their own comments
  - Show edit history indicator
  - 15-minute edit window
- [ ] Allow users to delete their own comments
- [ ] Allow listing owner to delete any comments
- [ ] Show "edited" indicator on edited comments

### Notifications
- [ ] Notify listing owner of new comments
- [ ] Notify comment author of replies
- [ ] Email notifications (with opt-out option)
- [ ] In-app notifications

## Technical Requirements

### Frontend
- [ ] Real-time comment posting (no page reload)
- [ ] Markdown or basic text formatting
- [ ] Loading states for comment actions
- [ ] Error handling with user feedback
- [ ] Responsive design for comment section

### Backend
- [ ] Comment validation
  - No empty comments
  - Length limits
  - Spam detection
- [ ] Rate limiting for comment posting
- [ ] Proper indexing for comment queries
- [ ] Efficient pagination

### Security
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Input sanitization
- [ ] Permission checking
- [ ] Rate limiting
- [ ] Spam protection

## User Flow

### Adding Comment
1. User navigates to listing detail
2. User scrolls to comment section
3. User enters comment text
4. System validates input
5. User submits comment
6. Comment appears in list
7. Notifications sent

### Editing Comment
1. User clicks edit on their comment
2. Form shows with current text
3. User modifies text
4. System validates changes
5. User saves changes
6. Updated comment displayed

### Deleting Comment
1. User clicks delete on their comment
2. Confirmation modal appears
3. User confirms deletion
4. Comment removed from list

## Error Scenarios
- [ ] Handle network errors during posting
- [ ] Handle validation errors
- [ ] Handle concurrent edits
- [ ] Handle deleted listings
- [ ] Handle banned users
- [ ] Handle rate limit exceeded

## Dependencies
- User authentication system
- Notification system
- Email service
- Text formatting library
- Spam detection service

## Definition of Done
- [ ] All acceptance criteria met
- [ ] Comment CRUD operations working
- [ ] Notifications functioning
- [ ] Real-time updates working
- [ ] Security measures implemented
- [ ] Rate limiting configured
- [ ] Error handling complete
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Performance requirements met
- [ ] Documentation updated
- [ ] Code reviewed and approved
- [ ] Mobile responsiveness verified
- [ ] Accessibility requirements met

## Notes for Developers
- Consider implementing WebSocket for real-time updates
- Implement proper caching strategy
- Consider implementing comment threading for future
- Ensure proper database indexing
- Implement comment moderation system
- Consider implementing emoji reactions
- Follow accessibility guidelines for forms 