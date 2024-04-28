import React from 'react'

const Hero = () => {
  return (
    <div className="bg-custom-beige">
      <textarea class="fm-editor-textarea" tabindex="2" placeholder="Dear Future Me..." id="letter_body" data-word-counter-target="input" data-action="focus->letter-editor#bodyFocused blur->letter-editor#bodyBlurred word-counter#count tealium-events#trackTealiumEvent:capture:once letter-editor#hideInspiration" data-tealium-events-event-name-param="letter_writing_started" data-tealium-events-payload-param="{&quot;user_id&quot;:&quot;12173842&quot;,&quot;user_is_premium&quot;:&quot;0&quot;,&quot;user_days_old&quot;:&quot;13&quot;,&quot;user_letters_count&quot;:&quot;2&quot;,&quot;user_payments_count&quot;:&quot;0&quot;}" data-letter-editor-inspiration-display-threshold-param="250" name="letter[body]">
</textarea>
    </div>
  )
}

export default Hero
