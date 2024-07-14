/** @odoo-module **/

import Widget from 'web.Widget';

/**
 * This widget represents a box that has been generated by the OCR. Such a box
 * is inserted on a box layer on a specific location. A box is related to
 * a field, and can be selected by the user and/or chosen by the OCR.
 */
var InvoiceExtractBox = Widget.extend({
    events: {
        'click': '_onClick'
    },
    template: 'account_invoice_extract.Box',
    /**
     * @override
     * @param {web.Class} parent class with EventDispatcherMixin
     * @param {Object} data
     * @param {float} data.box_angle angle in degrees for this box.
     * @param {float} data.box_height height of the box.
     * @param {float} data.box_midX x-coordinate of the middle point of this
     *   box.
     * @param {float} data.box_midY y-coordinate of the middle point of this
     *   box.
     * @param {float} data.box_width width of the box.
     * @param {string} data.feature name of the field that this box is related
     *   to.
     * @param {integer} data.id server-side ID of the box.
     * @param {integer} data.selected_status if not 0, this is chosen by the
     *   OCR.
     * @param {boolean} data.user_selected tell whether this box is selected by
     *   the user or not (server-side information).
     * @param {$.Element} data.$boxLayer jQuery element linked to the node of
     *   the box layer. This is used in order to compute the exact position of
     *   this box on the page.
     */
    init: function (parent, data) {
        this._super.apply(this, arguments);

        this._angle = data.box_angle;
        this._fieldName = data.feature;
        this._height = data.box_height;
        this._id = data.id;
        this._isOcrChosen = data.selected_status !== 0;
        this._isSelected = data.user_selected;
        this._midX = data.box_midX;
        this._midY = data.box_midY;
        this._text = data.text;
        this._width = data.box_width;
        this._$boxLayer = data.$boxLayer;
    },
    /**
     * Warn the invoice extract field that OCR chosen or selected boxes must be
     * tracked. This is useful in order to determine which box is selected.
     *
     * @override
     */
    start: function () {
        if (this._isSelected) {
            this.trigger_up('select_invoice_extract_box', {
                box: this,
            });
        }
        if (this._isOcrChosen) {
            this.trigger_up('choice_ocr_invoice_extract_box', {
                box: this,
            });
        }
        return this._super.apply(this, arguments);
    },
    /**
     * Warn the invoice extract field that this box should be untracked. This
     * is useful in order to keep using the same invoice extract field on
     * another invoice, which surely contains different boxes.
     *
     * @override
     */
    destroy: function () {
        this.trigger_up('destroy_invoice_extract_box', {
            box: this,
        });
        this._super.apply(this, arguments);
    },

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * Get the field name of this box.
     *
     * @returns {string}
     */
    getFieldName: function () {
        return this._fieldName;
    },
    /**
     * Get the server-side ID of this box.
     *
     * @returns {integer}
     */
    getID: function () {
        return this._id;
    },
    /**
     * Get the style of this box, which is useful to represent the box at the
     * exact position and box size on the box layer.
     *
     * @returns {string}
     */
    getStyle: function () {
        return 'left:' + (this._midX * parseInt(this._$boxLayer[0].style.width)) + 'px;' +
               'top:' + (this._midY * parseInt(this._$boxLayer[0].style.height))  + 'px;' +
               'width:' + ((this._width) * parseInt(this._$boxLayer[0].style.width)) + 'px;' +
               'height:' + ((this._height) * parseInt(this._$boxLayer[0].style.height))  + 'px;' +
               'transform: translate(-50%, -50%) rotate(' + this._angle + 'deg);' +
               '-ms-transform: translate(-50%, -50%) rotate(' + this._angle + 'deg);' +
               '-webkit-transform: translate(-50%, -50%) rotate(' + this._angle + 'deg);';
    },
    /**
     * Tells whether the box has been chosen by the OCR or not.
     *
     * @returns {boolean}
     */
    isOcrChosen: function () {
        return this._isOcrChosen;
    },
    /**
     * @returns {boolean}
     */
    isSelected: function () {
        return this._isSelected;
    },
    /**
     * Set this box as 'selected'. This is called by the field that is tracking
     * boxes. Indeed, an OCR box without any user-selected box should be
     * selected.
     */
    setSelected: function () {
        if (!this._isSelected) {
            this._isSelected = true;
            this.$el.addClass('selected');
        }
    },
    /**
     * Unset this box as 'ocr chosen'. This case occurs when this box is
     * unselected when no other box is selected. This behaviour matches the
     * server-side behaviour.
     */
    unsetOcrChosen: function () {
        if (this._isOcrChosen) {
            this._isOcrChosen = false;
            this.$el.removeClass('ocr_chosen');
        }
    },
    /**
     * Unset this box as 'selected'. This is called by the field that is
     * tracking boxes. Indeed, an OCR box without any user-selected box should
     * be selected. When another box is selected by the user, the OCR chosen
     * box should no longer be selected.
     */
    unsetSelected: function () {
        if (this._isSelected) {
            this._isSelected = false;
            this.$el.removeClass('selected');
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Called when clicking on this box.
     *
     * @private
     * @param {MouseEvent} ev
     */
    _onClick: function (ev) {
        ev.stopPropagation();
        this.trigger_up('click_invoice_extract_box', {
            box: this,
        });
    },
});

export default InvoiceExtractBox;