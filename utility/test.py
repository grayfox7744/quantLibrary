from win32com.client import Dispatch


def SendEmail(SendTo,CC,BCC,Subject,Body,Attachment=None,Pass=None):

    if SendTo==None:

        return

    session=Dispatch("Lotus.NotesSession")

    if Pass:

        session.Initialize(Pass)

    Server=session.GetEnvironmentString( "MailServer",True)

    MaildbName=session.GetEnvironmentString( "MailFile",True)

    db=session.GetDatabase(Server,MaildbName)

    doc=db.CreateDocument()

    doc.ReplaceItemValue("Form","Memo")

    if SendTo:

        doc.ReplaceItemValue("SendTo",SendTo)

    if CC:

        doc.ReplaceItemValue("CopyTo",SendTo)

    if BCC:

        doc.ReplaceItemValue("BlindCopyTo",SendTo)

    if Subject:

        doc.ReplaceItemValue("Subject",Subject)



    stream=session.CreateStream()

    stream.WriteText(Body)



    bodyMime=doc.CreateMIMEEntity()

    bodyMime.SetContentFromText(stream,"text/html;charset=iso-8859-1",False)



    if Attachment:

        RichTextItem = doc.CreateRichTextItem("Attachment")

        for fn in Attachment:

            RichTextItem.EmbedObject(1454, "", fn ,"Attachment")



    '''

    bodyMime=doc.CreateMIMEEntity()

    bodyMime.SetContentFromText(stream,"text/html;charset=iso-8859-1",False)

    doc.ReplaceItemValue( "Logo", "StdNotesLtr3" )

    doc.ReplaceItemValue( "_ViewIcon", 23 )

    doc.ReplaceItemValue( "SenderTag", "Y" )

    '''



    doc.Send(False)